from django.urls import path, include
from rest_framework import routers

from . import views

urlpatterns = [
    path('', views.home, name='app-home'),
    path('about/', views.about, name='app-about'),
    path('about_update/', views.about_update, name='app-about-update'),
    path('about_bot/', views.about_bot, name='app-about_bot'),
    path('api/', views.SoftwareApi.as_view(), name='app-api')
]
