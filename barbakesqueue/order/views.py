from django.shortcuts import render
from django.views import generic
from .models import *
from .forms import *
from customer.models import *
# Create your views here.

# make sure that only authenticated users can access this view
class Cart_form(generic.CreateView):
    model = Cart
    form_class = AddToCartForm

    def form_valid(self, form):
        '''
            get the current user customer id
        '''
        customer_instance = customer.objects.filter(user = self.request.user)
        
        # added the customer_instance of current user to the form instance
        form.instance.customer = customer_instance 
        
        return super().form_valid(form)
  
