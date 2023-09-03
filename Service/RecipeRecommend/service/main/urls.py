from django.contrib import admin
from django.urls import path
from .views import views


app_name = 'main'
urlpatterns = [
    path('', views.index, name="index"),
    path('views/', views.index, name='index'),
    path('recent/', views.index, name='index'),
    path('prefer/', views.index, name='index'),
    path('recommend/', views.recommend, name="recommend"),
    path('withs/<int:food_id>/', views.withs, name="withs"),
]