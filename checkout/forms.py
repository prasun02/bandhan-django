from django import forms

from accounts.models import Address
from core.forms import StyledFormMixin


class GuestCheckoutForm(StyledFormMixin, forms.Form):
    autocomplete = {
        "email": "email",
        "full_name": "name",
        "phone": "tel",
        "alternative_phone": "tel",
        "division": "address-level1",
        "district": "address-level2",
        "postal_code": "postal-code",
        "road": "street-address",
    }
    placeholders = {
        "email": "you@example.com",
        "full_name": "Full name",
        "phone": "01XXXXXXXXX",
        "division": "Dhaka",
        "district": "Dhaka",
        "upazila": "Dhanmondi",
        "area": "Area or neighborhood",
        "road": "Road, village, or street",
    }

    email = forms.EmailField(required=False)
    full_name = forms.CharField(max_length=160)
    phone = forms.CharField(max_length=32)
    alternative_phone = forms.CharField(max_length=32, required=False)
    division = forms.CharField(max_length=80)
    district = forms.CharField(max_length=80)
    upazila = forms.CharField(max_length=80, label="Upazila / Thana")
    area = forms.CharField(max_length=120)
    road = forms.CharField(max_length=160, label="Road / Village")
    house = forms.CharField(max_length=80, required=False, label="House / Holding")
    postal_code = forms.CharField(max_length=20, required=False)
    landmark = forms.CharField(max_length=160, required=False)
    delivery_instructions = forms.CharField(widget=forms.Textarea, required=False)
    label = forms.ChoiceField(choices=Address.Label.choices)
    delivery_zone = forms.ChoiceField(choices=())
    payment_method = forms.ChoiceField(choices=[("cod", "Cash on Delivery"), ("bkash", "bKash"), ("card", "Card")])
    terms = forms.BooleanField(label="I agree to the terms and return policy")
    idempotency_token = forms.CharField(max_length=120, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        zones = kwargs.pop("zones", None)
        super().__init__(*args, **kwargs)
        if zones is not None:
            self.fields["delivery_zone"].choices = [(zone.id, f"{zone.name} - {zone.delivery_estimate}") for zone in zones]
