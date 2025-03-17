# myapp/context_processors.py
from django.urls import reverse

def navigation_context(request):
    
    # get the current url
    url = request.path
    
    if url == reverse('main:cake_page'):
        return { 'cake_active' : 'active' } # return variable cake_active
    
    if url == reverse('account:login'):
        return { 'is_login_page' : True, 'xxx': 'variavle' } # for login page varibales    

    
    return {} # return nothing
