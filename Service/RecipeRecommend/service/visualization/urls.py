from django.contrib import admin
from django.urls import path
from . import views


app_name = 'visualization'
urlpatterns = [
    path('find', views.find, name="find"),
]