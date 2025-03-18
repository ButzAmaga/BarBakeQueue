# myapp/context_processors.py
from django.urls import reverse

def navigation_context(request):
    
    # get the current url
    url = request.path
    
    if url == reverse('order:orders'):
        return { 'orders_active' : 'active' } # return variable orders_active
    
    if url == reverse('chat:main'):
         
        return { 'messages_active' : 'active'} # return variable chat_active    

    
    return {} # return nothing
