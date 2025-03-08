from django.shortcuts import render
from django.views import generic
from .models import *
from .forms import *
from customer.models import *
from django.shortcuts import get_object_or_404
from django.views.generic.detail import SingleObjectMixin
from cake.models import *
from django.urls import reverse_lazy
# Create your views here.

class CakeDetailMixin(SingleObjectMixin):
    model = Cake
    
    def get_object(self, queryset=None):
        #Fetch the specific Cake that the user is adding to the cart.
        return get_object_or_404(Cake, pk=self.kwargs["pk"])  # Get Cake from URL
    


class Cart_Created(generic.TemplateView):
    template_name = "order/cart/created_cart.html"

# make sure that only authenticated users can access this view
class Cart_form(CakeDetailMixin, generic.CreateView):
    form_class = AddToCartForm
    model = Cart
    template_name = "order/cart/customize_cake.html"
    success_url = reverse_lazy("order:cart_created")
    
    def get_context_data(self, **kwargs):
        """Add the Cake object to the context alongside the form."""
        context = super().get_context_data(**kwargs)
        context["cake"] = self.get_object()  # Pass Cake to template
        return context
    
    def form_valid(self, form):
        '''
            get the current user customer id
        '''


        customer_instance = customer.objects.get(account = self.request.user)
        
        # added the customer_instance of current user to the form instance
        form.instance.customer = customer_instance 
        
        # set the cake instance to the form instance
        form.instance.cake = self.get_object()
        
        return super().form_valid(form)
  
