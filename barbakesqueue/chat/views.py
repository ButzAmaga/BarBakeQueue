from django.shortcuts import render
from django.views.generic import TemplateView, FormView, ListView, DetailView
from django.contrib.auth.models import User, Group
from django.urls import reverse_lazy
from .forms import *
# Create your views here.


class Index(ListView):
    template_name = 'chat/index.html'
    model = User 
    context_object_name = "customers"
    
    def get_queryset(self):
        
        customers = self.model.objects.filter(groups__name="Customer")
        
        return customers
    

class Room(DetailView):
    template_name = 'chat/chatroom_2.html'
    model = User
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["chatroom"] = kwargs.get('chatroom')
        
        return context

class PersonFormView(FormView):
    template_name = "chat/person_form.html"    
    form_class = PersonForm
    success_url = reverse_lazy('htmx')