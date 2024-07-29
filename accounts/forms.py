from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import (
    UserCreationForm as BaseUserCreationForm,
    AuthenticationForm as BaseAuthenticationForm,
)

from accounts.models import User
from utils.constants import INPUT_CLASS, SELECT_CLASS


class UserCreationForm(BaseUserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text="Required. Inform a valid email address.",
        widget=forms.EmailInput(attrs={"placeholder": "Email", **INPUT_CLASS}),
    )
    password1 = forms.CharField(
        label="Password",
        help_text=password_validation.password_validators_help_text_html(),
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "placeholder": "Password",
                **INPUT_CLASS,
            }
        ),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "placeholder": "Confirm Password",
                **INPUT_CLASS,
            }
        ),
    )

    class Meta(BaseUserCreationForm.Meta):
        model = User
        fields = ["username", "email", "role"]
        widgets = {
            "username": forms.TextInput(
                attrs={"placeholder": "Username", **INPUT_CLASS}
            ),
            "password2": forms.PasswordInput(
                attrs={"placeholder": "Password", **INPUT_CLASS}
            ),
            "role": forms.Select(attrs={**SELECT_CLASS}),
        }

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Email already registered")
        return email


class AuthenticationForm(BaseAuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields["username"].widget.attrs.update({**INPUT_CLASS})
        self.fields["password"].widget.attrs.update({**INPUT_CLASS})
