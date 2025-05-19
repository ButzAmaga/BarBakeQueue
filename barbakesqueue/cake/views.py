from django.shortcuts import render
from django.views import generic
from .models import Cake
from common.views import LoginWithPermissionMixin
from .forms import *
# Create your views here.

class CakeList(LoginWithPermissionMixin, generic.ListView):
    model = Cake
    template_name = "cake/cake_management.html"
    context_object_name = "cakes"
    
    def get_queryset(self):
        return self.model.objects.all().order_by("group_by") 
    

class CakeEdit(LoginWithPermissionMixin, generic.UpdateView):
    model = Cake
    template_name = "cake/cake_edit.html"
    form_class = CakeForm