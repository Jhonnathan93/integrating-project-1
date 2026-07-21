from django.urls import path

from . import views

app_name = "book"

urlpatterns = [
    path("", views.index, name="home"),
    path("index/", views.index, name="index"),
    path("recommendations/", views.recommendations, name="recommendations"),
    path("response/", views.response, name="response"),
    path(
        "mark-as-not-recommended/",
        views.mark_as_not_recommended,
        name="mark-as-not-recommended",
    ),
    path("faq/", views.faq, name="faq"),
]
