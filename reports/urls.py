from django.contrib import admin
from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.reports, name = 'report')
]