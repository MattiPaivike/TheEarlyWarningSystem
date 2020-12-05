from django.shortcuts import render
from django.http import HttpResponse
from main_app.models import Software, Version
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import viewsets, mixins

#import restframework authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import SoftwareSerializer

class SoftwareApi(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SoftwareSerializer
    def get(self, request):
        queryset = Version.objects.all()
        serializer = SoftwareSerializer(queryset, many=True)
        return Response(serializer.data)

def home(request):
    page = 'home'
    applications = Version.objects.all()
    appscount = Version.objects.all().count()
    return render(request, 'main_app/apps.html', locals())

def about(request):
    page = 'about'
    return render(request, 'main_app/about.html', locals())

def about_update(request):
    page = 'about_update'
    return render(request, 'main_app/about_update.html', locals())

def about_bot(request):
    page = 'about_bot'
    return render(request, 'main_app/about_bot.html', locals())
