from django.forms import forms
from .models import *

'''
    form for adding a cake to the cart of the user
'''
class AddToCartForm(forms.ModelForm):
    
    class Meta:
        model = Cart
        fields = "__all__"
        
        
    
