from django import forms 
from order.models import Order

from .models import Transaction

# customer transaction form
class TransactionForm(forms.ModelForm):
    
    class Meta:
        model = Transaction
        exclude = ["order_id","status"]
   
    def __init__(self, *args, **kwargs):
       self.order_id = kwargs.pop("order_id") # already the instance of the object
       super().__init__(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        '''
            get the order instance and bind it to the created transaction instance then save
        '''
        instance = super().save(commit=False, *args, **kwargs)

        instance.order_id = self.order_id

        instance.save()


