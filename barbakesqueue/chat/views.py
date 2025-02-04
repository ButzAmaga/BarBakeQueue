from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from .forms import *
# Create your views here.


class Index(TemplateView):
    template_name = 'chat/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] =  PersonForm
        return context
    

class Room(TemplateView):
    template_name = 'chat/chatroom.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["chatroom"] = kwargs.get('chatroom')
        
         
        return context

class PersonFormView(FormView):
    template_name = "chat/person_form.html"    
    form_class = PersonForm
    success_url = reverse_lazy('htmx')