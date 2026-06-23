from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [path("track/", views.track_order, name="track")]
