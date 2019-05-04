from django.urls import path
from rest_framework import routers

from . import views

urlpatterns = [
    path('', views.home, name='app-home'),
    path('about/', views.about, name='app-about'),
    path('api/', include(router.urls))
]
