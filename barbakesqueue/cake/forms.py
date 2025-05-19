from django import forms
from .models import *


class CakeForm(forms.ModelForm):
    class  Meta():
        model = Cake
        fields = "__all__"
        

        
