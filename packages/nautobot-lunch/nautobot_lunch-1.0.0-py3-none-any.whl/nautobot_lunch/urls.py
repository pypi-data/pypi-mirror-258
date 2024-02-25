"""Django urlpatterns declaration for nautobot_lunch app."""

from django.urls import path

from nautobot_lunch import views

urlpatterns = [
    path("locations/<uuid:pk>/lunch-tab", views.LocationDetailPluginLunchTab.as_view(), name="location_detail_lunch"),
]
