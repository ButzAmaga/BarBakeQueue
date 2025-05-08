from django import forms
from .models import *


class CustomerRatingForm(forms.ModelForm):
    class  Meta():
        model = Rating
        exclude = ["cake", "customer"]
        
        widgets = {
            "rate" : forms.RadioSelect()
        }
    
    def __init__(self, *args, **kwargs):
       self.customer = kwargs.pop("customer") 
       self.cake = kwargs.pop("cake")
       super().__init__(*args, **kwargs)
       
    def save(self, *args, **kwargs):
        instance = super().save(commit=False, *args, **kwargs)

        instance.cake = self.cake 
        instance.customer = self.customer
        
        instance.save()
