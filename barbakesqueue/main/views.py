from django.shortcuts import render
from django.views.generic import TemplateView,ListView
from cake.models import *
# Create your views here.

class Cake_page(ListView):
    template_name = 'main/cake_page.html'
    model = Cake
    context_object_name = 'cakes'
