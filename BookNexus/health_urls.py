"""Infrastructure endpoint routes for the BookNexus project."""

from django.urls import path

from BookNexus.health import health

app_name = "health"

urlpatterns = [
    path("", health, name="health"),
]
