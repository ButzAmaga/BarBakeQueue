from django import forms
from .models import *


class ChangeStatusForm(forms.ModelForm):
    class  Meta():
        model = Order
        fields = ["status"]
        

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


""" 
    For setting delivery date and etc for the order
"""    

class OrderForm(forms.Form):
    
    date_delivery = forms.DateField(initial=date.today(),widget=forms.DateInput(attrs={"type":"date"}))
    
    def clean_date_delivery(self):
        """
            the delivery date must be 7 days
        """ 
        field = self.cleaned_data["date_delivery"]
        
        if field < date.today() + timedelta(days=7):
            raise forms.ValidationError("Date must be at least 7 days from now")
        
        return field 
    
    def get_date_delivery(self):
        return self.cleaned_data["date_delivery"]
            

orderBaseModelFormSet = forms.modelformset_factory(Cart, form=AddToOrderForm,  extra=0) 

class OrderFormSet(orderBaseModelFormSet):
    def clean(self):
        """ if there is no cart marked raise an error """ 
        if not self.has_changed():
            raise forms.ValidationError("No cart item have been ordered")

        return super().clean()

    
        
    
