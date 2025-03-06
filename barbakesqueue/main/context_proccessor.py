# myapp/context_processors.py
from django.urls import reverse

def navigation_context(request):
    
    # get the current url
    url = request.path
    
    if url == reverse('main:index'):
        return { 'home_active' : 'active' } # return variable home_active
    
    if url == reverse('account:login'):
        return { 'is_login_page' : True, 'xxx': 'variavle' } # for login page varibales    

    
    return {} # return nothing
