from django import forms
from .models import *

'''
    form for adding a cake to the cart of the user
'''
class AddToCartForm(forms.ModelForm):
    
    class Meta:
        model = Cart
        exclude = ["cake", "customer"]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["quantity"].initial = 1
        
        
    
