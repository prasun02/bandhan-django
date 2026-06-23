from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import TemplateView

from catalog.sitemaps import ProductSitemap, StaticViewSitemap
from core import views as core_views

sitemaps = {"products": ProductSitemap, "static": StaticViewSitemap}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", core_views.home, name="home"),
    path("", include("catalog.urls")),
    path("cart/", include("cart.urls")),
    path("checkout/", include("checkout.urls")),
    path("accounts/", include("accounts.urls")),
    path("orders/", include("orders.urls")),
    path("reviews/", include("reviews.urls")),
    path("returns/", include("returns.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path("about/", TemplateView.as_view(template_name="pages/about.html"), name="about"),
    path("contact/", core_views.contact, name="contact"),
    path("faq/", TemplateView.as_view(template_name="pages/faq.html"), name="faq"),
    path("size-guide/", TemplateView.as_view(template_name="pages/size_guide.html"), name="size_guide"),
    path("delivery-policy/", TemplateView.as_view(template_name="pages/delivery_policy.html"), name="delivery_policy"),
    path("return-refund-policy/", TemplateView.as_view(template_name="pages/return_policy.html"), name="return_policy"),
    path("privacy-policy/", TemplateView.as_view(template_name="pages/privacy.html"), name="privacy"),
    path("terms-and-conditions/", TemplateView.as_view(template_name="pages/terms.html"), name="terms"),
    path("payment-instructions/", TemplateView.as_view(template_name="pages/payment_instructions.html"), name="payment_instructions"),
]

handler404 = "core.views.custom_404"
handler500 = "core.views.custom_500"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
