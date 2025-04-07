from django import forms
from .models import *

'''
    form for customer registration
'''
class Customer_registration_form(forms.ModelForm):
    
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20)
     
    class Meta:
        model = customer
        exclude = ["account"]
        
