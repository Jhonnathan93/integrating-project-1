from django.urls import path

from . import views

app_name = "readinglists"

urlpatterns = [
    path("overview/", views.overview, name="overview"),
    path(
        "overview/<int:reading_list_id>/",
        views.detail,
        name="readinglist_detail",
    ),
    path("createlist/", views.create_list, name="createlist"),
    path("deletelist/<int:reading_list_id>/", views.delete_list, name="deletelist"),
    path("readinglist/<int:reading_list_id>/", views.detail, name="detail"),
    path(
        "deletebook/<int:reading_list_id>/<int:book_id>/",
        views.delete_book,
        name="deletebook",
    ),
    path(
        "editreadinglist/<int:reading_list_id>",
        views.update_reading_list,
        name="updatereadinglist",
    ),
    path("add-to-list/", views.add_to_reading_list, name="add-to-list"),
]
