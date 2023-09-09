"""
URL configuration for BookNexus project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from book import views as BookViews
from django.conf import settings
from django.conf.urls.static import static
import openai
import os

api_key = "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"


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", BookViews.index),
    path("recomendations/", BookViews.recomendations),
    path("index/", BookViews.index),
    path("profile/", BookViews.profile),
    path('response/', BookViews.response, name='response'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

