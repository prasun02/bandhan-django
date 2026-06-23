from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from cart.services import merge_session_cart

from .forms import AddressForm, RegistrationForm, StyledAuthenticationForm, StyledPasswordResetForm, StyledSetPasswordForm
from .models import CustomerProfile


class EmailLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = StyledAuthenticationForm


class EmailLogoutView(LogoutView):
    pass


class CustomerPasswordResetView(PasswordResetView):
    template_name = "accounts/password_reset.html"
    email_template_name = "accounts/password_reset_email.html"
    form_class = StyledPasswordResetForm
    success_url = reverse_lazy("accounts:password_reset_done")


class CustomerPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "accounts/password_reset_confirm.html"
    form_class = StyledSetPasswordForm
    success_url = reverse_lazy("accounts:login")


def register(request):
    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        CustomerProfile.objects.get_or_create(user=user)
        login(request, user)
        merge_session_cart(request, user)
        response = redirect("accounts:dashboard")
        if request.headers.get("HX-Request"):
            response["HX-Redirect"] = response.url
        return response
    return render(request, "accounts/register.html", {"form": form})


@login_required
def dashboard(request):
    return render(request, "accounts/dashboard.html")


@login_required
def addresses(request):
    form = AddressForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        address = form.save(commit=False)
        address.user = request.user
        address.save()
        return redirect("accounts:addresses")
    return render(request, "accounts/addresses.html", {"form": form, "addresses": request.user.addresses.all()})
