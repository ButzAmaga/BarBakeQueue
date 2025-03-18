from django import forms
from .models import *

'''
    form for adding a cake to the cart of the user
'''
class AddToCartForm(forms.ModelForm):
    
    class Meta:
        model = Cart
        exclude = ["cake", "customer", "order_id", "is_ordered"]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["quantity"].initial = 1
        

class AddToOrderForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ["is_ordered"]
        # fields = '__all__'


    

orderBaseModelFormSet = forms.modelformset_factory(Cart, form=AddToOrderForm,  extra=0) 

class OrderFormSet(orderBaseModelFormSet):
    def clean(self):
        """ if there is no cart marked raise an error """ 
        if not self.has_changed():
            raise forms.ValidationError("No cart item have been ordered")

        return super().clean()

    
        
    
