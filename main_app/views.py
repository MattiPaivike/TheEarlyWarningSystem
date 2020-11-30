from django.shortcuts import render
from django.http import HttpResponse
from main_app.models import Software, Version
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import viewsets, mixins
from .serializers import SoftwareSerializer

class SoftwareApi(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Version.objects.all()
    serializer_class = SoftwareSerializer

def home(request):
    page = 'home'
    applications = Version.objects.all()
    appscount = Version.objects.all().count()
    return render(request, 'main_app/apps.html', locals())

def about(request):
    page = 'about'
    return render(request, 'main_app/about.html', locals())

def about_bot(request):
    page = 'about_bot'
    return render(request, 'main_app/about_bot.html', locals())
