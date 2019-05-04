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
    applications = Version.objects.all()
    appscount = Version.objects.all().count()
    page = 'home'
    return render(request, 'main_app/apps.html', locals())

def about(request):
    page = 'about'
    return render(request, 'main_app/about.html', locals())


#leaving this here for future use
#paginator = Paginator(applications, 10)
#page = request.GET.get('page', 1)
#try:
#    applications = paginator.page(page)
#except PageNotAnInteger:
#    applications = paginator.page(1)
#except EmptyPage:
#    applications = paginator.page(paginator.num_pages)
