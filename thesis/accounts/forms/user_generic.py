from django import forms
from django.contrib.auth.forms import UserCreationForm
# from freelancing.models.user_generic import UserGeneric


class UserGenericCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True, label="Prénom")
    last_name = forms.CharField(required=True, label="Nom")
    accept_terms = forms.BooleanField(required=False, label="CGU")
    newsletter = forms.BooleanField(required=False, label="Newsletter")
    CHECKBOX_M_Mme = (
        ("M", "M"),
        ("Mme", "Mme"),
    )
    gender = forms.ChoiceField(
        choices=CHECKBOX_M_Mme,
        widget=forms.RadioSelect,
        label="",
        required=False,
    )

    class Meta(UserCreationForm):
        # model = UserGeneric
        fields = (
            # "username",
            "email",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "gender",
            "newsletter",
        )

    def clean(self):
        super(UserCreationForm, self).clean()
        data = self.cleaned_data
        if not data["accept_terms"]:
            msg = "Veuillez lire et accepter les CGUs avant de continuer"
            self.add_error("accept_terms", msg)


class UserGenericUpdateForm(forms.ModelForm):
    first_name = forms.CharField(required=True, label="Prénom*")
    last_name = forms.CharField(required=True, label="Nom*")
    disabled_fields = ("email",)

    class Meta:
        # model = UserGeneric
        fields = ("email", "first_name", "last_name", "gender")

    def __init__(self, *args, **kwargs):
        super(UserGenericUpdateForm, self).__init__(*args, **kwargs)
        for field in self.disabled_fields:
            self.fields[field].disabled = True


class ProfileSignUpForm(forms.Form):
    first_name = forms.CharField(required=True, label="Prénom")
    last_name = forms.CharField(required=True, label="Nom")
    phone_number = forms.CharField(required=False, label="N° de téléphone portable")
    skype_contact = forms.CharField(required=False, label="Contact Skype")
    portfolio_link = forms.CharField(required=False, label="Lien vers vos travaux")
    budget = forms.CharField(required=False, label="Tarif (en cts/mot)")
    comment_inscription = forms.Textarea()

    class Meta(UserCreationForm):
        # model = UserGeneric
        fields = (
            # "username",
            "email",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "phone_number",
            "skype_contact",
            "activity_sector",
            "budget",
            "comment_inscription",
        )
