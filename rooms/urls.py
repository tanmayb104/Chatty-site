from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('createroom/', views.createroom, name="createroom"),
    path('joinroom/', views.joinroom, name="joinroom"),
    path('', views.rooms, name="rooms"),
    path('searchroom/', views.searchroom, name="searchroom"),
    path('room/<str:code>/', views.detailroom, name="detailroom"),
    path('room/<str:code>/join/', views.joinmeeting, name="joinmeeting"),
    path('settings/', views.settings, name="settings"),
]