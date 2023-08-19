# External imports
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.http import HttpResponse
import requests

# Internal imports
from accounts.forms.user_generic import UserGenericCreationForm
# from freelancing.models.freelance import Freelance
# from freelancing.models.haskn_logo import HasknLogo
# from freelancing.my_utils.my_emails import email_sign_up_success, email_resset_password

# Imports for password reset
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.views import (
    LoginView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.urls import reverse_lazy
from django.contrib import messages

User = get_user_model()

"""
    Overriding django.contrib.auth.views to send background
    image to base_login.html
"""


class MyLoginView(LoginView):
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super(MyLoginView, self).get_context_data()
        context["haskn_logo"] = HasknLogo.take_logo()
        return context

    def get_success_url(self):
        return reverse_lazy("index")

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password")
        return self.render_to_response(self.get_context_data(form=form))


class MyPasswordResetDoneView(PasswordResetDoneView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # needed to redirect to haskn own template
        self.template_name = "registration/lost_password_sent.html"

    def get_context_data(self, **kwargs):
        context = super(MyPasswordResetDoneView, self).get_context_data()
        context["haskn_logo"] = HasknLogo.take_logo()
        return context


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # needed to redirect to haskn own template
        self.template_name = "registration/lost_password_reset_form.html"

    def get_context_data(self, **kwargs):
        context = super(MyPasswordResetConfirmView, self).get_context_data()
        context["haskn_logo"] = HasknLogo.take_logo()
        return context


class MyPasswordResetCompleteView(PasswordResetCompleteView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # needed to redirect to haskn own template
        self.template_name = "registration/lost_password_complete.html"

    def get_context_data(self, **kwargs):
        context = super(MyPasswordResetCompleteView, self).get_context_data()
        context["haskn_logo"] = HasknLogo.take_logo()
        return context


def signup(request):
    return render(request, "registration/signup.html", {})


def general_conditions(request):
    return render(
        request, "registration/general_conditions/general_conditions.html", {}
    )


class SignUpView(CreateView):
    form_class = UserGenericCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def get_context_data(self, **kwargs):
        context = super(SignUpView, self).get_context_data()
        context["haskn_logo"] = HasknLogo.take_logo()
        return context

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        user = form.save(commit=False)

        # redirect to fill the recaptcha when it's empty
        if self.request.POST.get("g-recaptcha-response") is not None:
            token_recaptcha = self.request.POST["g-recaptcha-response"]
            if token_recaptcha == "":
                return self.render_to_response(self.get_context_data(form=form))

        # TODO: to test this in unit test, and
        #  put this field in the admin, not visible
        user.user_type = 3
        user.save()

        # Create Freelance object associated to this signup
        # remark that we don't have extra Freelance's info
        # besides the type_status
        messages.add_message(
            self.request, level=messages.SUCCESS, message="Utilisateur enregistré"
        )
        # creates a Freelance profile
        Freelance.objects.get_or_create(user=user)

        # accepting newsletter to freelance
        if self.request.POST.get("newsletter") is not None:
            if self.request.POST.get("newsletter") == "on":
                current_user = Freelance.objects.get(user=user)
                current_user.newsletter = True
                current_user.save()
        # send notification by email
        email_sign_up_success(user)

        return HttpResponseRedirect(self.success_url)


def validate_recaptcha_htmx(request):
    # to send the error msg to recaptcha
    template = "registration/snippets/recaptcha_validation.html"
    state_error = "Ce champ est obligatoire"
    context = {}
    recaptcha = request.POST["g-recaptcha-response"]
    if recaptcha == "":
        context = {"state_error": state_error}
    return render(request, template, context)


def password_reset_request(request):
    template_name = "registration/lost_password.html"
    success_url = reverse_lazy("reset_password")
    if request.method == "POST":

        password_form = PasswordResetForm(request.POST)
        if password_form.is_valid():

            # user_email = User.objects.filter(Q(email=password_form.data["email"]))
            data = password_form.cleaned_data["email"]
            user_email = User.objects.filter(Q(email=data))

            if user_email:
                for user in user_email:
                    email_template_name = "html_emails/reset_pssw_email_msg.html"
                    parameters = {
                        "email": user.email,
                        "user": user,
                        "domain": request.get_host(),
                        "site_name": "Haskn",
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "token": default_token_generator.make_token(user),
                        "protocol": "http",
                    }
                    email = render_to_string(email_template_name, parameters)
                    try:
                        email_resset_password(
                            user,
                            email,
                            host_name=request.get_host(),
                            uid=parameters["uid"],
                            token=parameters["token"],
                        )
                    except:
                        return HttpResponse("Invalid Header")

                    return redirect("password_reset_done")
            else:
                messages.add_message(
                    request,
                    level=messages.WARNING,
                    message="l'email saisi n'existe pas, veuillez en essayer un autre.",
                )
                return HttpResponseRedirect(success_url)
    else:
        password_form = PasswordResetForm()

    context = {
        "password_form": password_form,
        "haskn_logo": HasknLogo.take_logo(),
    }
    return render(request, template_name, context)
