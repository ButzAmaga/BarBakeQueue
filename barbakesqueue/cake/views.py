from django.shortcuts import render
from django.views import generic
from .models import Cake
from common.views import LoginWithPermissionMixin
from .forms import *
from django.urls import reverse_lazy
# Create your views here.

class CakeList(LoginWithPermissionMixin, generic.ListView):
    model = Cake
    template_name = "cake/cake_management.html"
    context_object_name = "cakes"
    
    def get_queryset(self):
        return self.model.objects.all().order_by("group_by") 

class CakeCreate(LoginWithPermissionMixin, generic.CreateView):
    model = Cake
    template_name = "cake/cake_create.html"
    form_class = CakeForm
    success_url = reverse_lazy("cake:cakes")

class CakeEdit(LoginWithPermissionMixin, generic.UpdateView):
    model = Cake
    template_name = "cake/cake_edit.html"
    form_class = CakeForm
    
    def get_success_url(self):
        return reverse_lazy("cake:edit", args = [self.kwargs["pk"]])

class CakeDelete(LoginWithPermissionMixin, generic.DeleteView):
    model = Cake
    template_name = "cake/cake_delete.html"
    success_url = reverse_lazy("cake:cakes")