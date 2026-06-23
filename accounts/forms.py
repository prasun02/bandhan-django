from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.forms import UserCreationForm

from core.forms import StyledFormMixin

from .models import Address, CustomerProfile, User


class RegistrationForm(StyledFormMixin, UserCreationForm):
    placeholders = {"full_name": "Your full name", "email": "you@example.com", "phone": "01XXXXXXXXX"}
    autocomplete = {"full_name": "name", "email": "email", "phone": "tel", "password1": "new-password", "password2": "new-password"}

    class Meta:
        model = User
        fields = ("full_name", "email", "phone")


class StyledAuthenticationForm(StyledFormMixin, AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput)
    placeholders = {"username": "you@example.com", "password": "Your password"}
    autocomplete = {"username": "email", "password": "current-password"}


class StyledPasswordResetForm(StyledFormMixin, PasswordResetForm):
    placeholders = {"email": "you@example.com"}
    autocomplete = {"email": "email"}


class StyledSetPasswordForm(StyledFormMixin, SetPasswordForm):
    autocomplete = {"new_password1": "new-password", "new_password2": "new-password"}


class StyledPasswordChangeForm(StyledFormMixin, PasswordChangeForm):
    autocomplete = {"old_password": "current-password", "new_password1": "new-password", "new_password2": "new-password"}


class ProfileForm(StyledFormMixin, forms.ModelForm):
    placeholders = {"full_name": "Your full name", "email": "you@example.com", "phone": "01XXXXXXXXX"}
    autocomplete = {"full_name": "name", "email": "email", "phone": "tel"}

    class Meta:
        model = User
        fields = ("full_name", "email", "phone")


class CustomerProfileForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ("alternative_phone", "profile_image", "date_of_birth", "marketing_consent")


class AddressForm(StyledFormMixin, forms.ModelForm):
    autocomplete = {
        "full_name": "name",
        "phone": "tel",
        "alternative_phone": "tel",
        "division": "address-level1",
        "district": "address-level2",
        "postal_code": "postal-code",
        "road": "street-address",
    }

    class Meta:
        model = Address
        exclude = ("user",)
