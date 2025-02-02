from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.


class Index(TemplateView):
    template_name = 'chat/index.html'

class Room(TemplateView):
    template_name = 'chat/chatroom.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["chatroom"] = kwargs.get('chatroom')
        
         
        return context
    