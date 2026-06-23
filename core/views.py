from django.core.mail import send_mail
from django.shortcuts import render

from catalog.selectors import home_products


def home(request):
    return render(request, "core/home.html", home_products())


def contact(request):
    sent = False
    if request.method == "POST":
        send_mail(
            subject=f"Bandhan contact: {request.POST.get('name', 'Customer')}",
            message=request.POST.get("message", ""),
            from_email=None,
            recipient_list=["support@example.com"],
            fail_silently=True,
        )
        sent = True
    return render(request, "pages/contact.html", {"sent": sent})


def custom_404(request, exception):
    return render(request, "404.html", status=404)


def custom_500(request):
    return render(request, "500.html", status=500)
