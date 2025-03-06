from django.shortcuts import render
from django.views.generic import TemplateView,ListView
from cake.models import *
# Create your views here.

class Index(ListView):
    template_name = 'main/index.html'
    model = Cake
    context_object_name = 'cakes'
