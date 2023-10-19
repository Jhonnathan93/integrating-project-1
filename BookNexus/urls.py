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
from django.urls import path, include

from book import views as BookViews
from readinglists import views as ReadingListViews
from newsletter import views as Newsletter
from analytics import views as Analytics

from django.conf import settings
from django.conf.urls.static import static

import openai
import os

api_key = ""

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', BookViews.index, name='home'),

    path('accounts/', include('accounts.urls')),
    path('reports/', include('reports.urls')),
    

    path("recomendations/", BookViews.recomendations),
    path("index/", BookViews.index),
    path('response/', BookViews.response, name='response'),

    path('overview/', ReadingListViews.overview, name='overview'),
    path('overview/<int:reading_list_id>/', ReadingListViews.detail, name='readinglist_detail'),
    path('createlist/', ReadingListViews.createlist, name='createlist'),
    path('deletelist/<int:reading_list_id>/', ReadingListViews.deletelist, name='deletelist'),
    path('readinglist/<int:reading_list_id>/', ReadingListViews.detail, name='detail'),
    path('deletebook/<int:reading_list_id>/<int:book_id>/', ReadingListViews.deletebook, name='deletebook'),
    path('editreadinglist/<int:reading_list_id>', ReadingListViews.updatereadinglist, name='updatereadinglist'),

    path('send_email_to_readers/', Newsletter.send_email_to_readers, name='send_email_to_readers'),
    path('newsletter/', Newsletter.top, name="newsletter"),

    path('top_books/', Analytics.top_books, name='top_books')

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
