from django.urls import path

from . import views

app_name = "newsletter"

urlpatterns = [
    path(
        "send_email_to_readers/",
        views.send_email_to_readers,
        name="send_email_to_readers",
    ),
]
