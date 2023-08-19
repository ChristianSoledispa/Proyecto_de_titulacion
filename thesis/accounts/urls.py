# accounts/urls.py
from django.urls import path
from accounts import views as views

# Authenticated view import NOTE: Iportant for sending emails
from django.contrib.auth import views as auth_views

from accounts.views import general_conditions
# from freelancing.models.haskn_logo import HasknLogo

urlpatterns = [
    # login's url must not change, see config in settings
    path("login", views.MyLoginView.as_view(), name="login"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    #         Authenticated views
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # path(
    #     "reset_password/",
    #     auth_views.PasswordResetView.as_view(
    #         template_name="registration/lost_password.html"
    #     ),
    #     name="reset_password",
    # ),
    path(
        "validate_recaptcha_htmx/",
        views.validate_recaptcha_htmx,
        name="validate_recaptcha_htmx",
    ),
    path(
        "reset_password/",
        views.password_reset_request,
        name="reset_password",
    ),
    path(
        "reset_password_sent/",
        views.MyPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "format/<uidb64>/<token>/",
        views.MyPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete/",
        views.MyPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path(
        "condition/",
        general_conditions,
        name="general_condition",
    ),
]
