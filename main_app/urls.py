from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('versions', views.SoftwareApi)

urlpatterns = [
    path('', views.home, name='app-home'),
    path('about/', views.about, name='app-about'),
    path('about_bot/', views.about_bot, name='app-about_bot'),
    path('api/', include(router.urls), name='app-api')
]
