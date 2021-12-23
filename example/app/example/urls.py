"""example URL Configuration
"""
from django.contrib import admin
from django.urls import path

import myapp
from myapp import views

urlpatterns = [
    path('', myapp.views.home, name='home'),
    path('more/', myapp.views.more, name='more'),
]
