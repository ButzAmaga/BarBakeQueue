from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Transaction
from order.models import Order
from .forms import TransactionForm
from django.urls import reverse_lazy
from django.contrib import messages
# Create your views here.


# customer order transaction form
class Customer_form(generic.CreateView):
    model = Transaction
    template_name = "transaction/customer_form.html"
    form_class = TransactionForm
    success_url = reverse_lazy("transaction:customer_form")
    # set up the initial value or order id of the form

    def get_success_url(self):
        return reverse_lazy("transaction:customer_form", kwargs={'order_id': self.kwargs.get('order_id')})
    
    def get_form_kwargs(self):
        '''
            Get the order object for the transaction and place it as kwargs for the form, raise 404 if the order 
            is not found
        ''' 
        data = super().get_form_kwargs()
        data["order_id"] = get_object_or_404(Order, id = self.kwargs.get("order_id", None))
        
        # save the fetched order instance for the template context
        self.order_instance = data["order_id"]
        
        return data 
    
    def get_context_data(self, **kwargs):
        """ 
            add the order instance to the template context
        """
        data = super().get_context_data(**kwargs)
        data["order"] = self.order_instance
        return data
    
    def form_valid(self, form):
        messages.success(self.request, "Successfully sent the prof of payment, please wait for verification. Thank you!")
        return super().form_valid(form)
    