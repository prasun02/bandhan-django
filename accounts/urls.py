from django.contrib.auth import views as auth_views
from django.urls import path

from .forms import StyledPasswordChangeForm
from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.EmailLoginView.as_view(), name="login"),
    path("logout/", views.EmailLogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("addresses/", views.addresses, name="addresses"),
    path("password-change/", auth_views.PasswordChangeView.as_view(template_name="accounts/password_change.html", form_class=StyledPasswordChangeForm), name="password_change"),
    path("password-reset/", views.CustomerPasswordResetView.as_view(), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", views.CustomerPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
]
