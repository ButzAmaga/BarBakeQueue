from django import forms
from .models import *


class CustomerRatingForm(forms.ModelForm):
    class  Meta():
        model = Rating
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
       self.customer = kwargs.pop("customer") 
       self.cake = kwargs.pop("cake")
       super().__init__(*args, **kwargs)
