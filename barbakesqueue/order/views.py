from django.shortcuts import render
from django.views import generic
from .models import *
from .forms import *
from customer.models import *
from django.shortcuts import get_object_or_404
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin
from cake.models import *
from django.urls import reverse_lazy
from django.db.models import Sum
# Create your views here.


# admin view

class Index(generic.TemplateView):
    template_name = "order/index.html"

class Get_unpaid_order(generic.ListView):
    model = Order
    template_name = "order/unpaid_order_instances.html"
    context_object_name = "orders"
    
    def get_queryset(self):
        ''' return all order that is not paid '''
        instances = self.model.objects.filter(status = "not paid").annotate(total_price = Sum("cart_items__cake__price") ).order_by("-date_ordered")
        return instances





# customer view 

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

  
class Cart_items(generic.ListView):
    model = Cart
    template_name = "order/cart/cart_items.html"
    context_object_name = 'cart_items'
    
    
    def get_queryset(self):
        '''
            get the current user customer id and then get the customer`s cart items, which are not ordered
        '''
        customer_id = customer.objects.get(account = self.request.user)
        items = self.model.objects.filter(customer = customer_id, is_ordered = False)
        
        return items

class Cart_items_v2(generic.FormView):
    form_class = OrderFormSet
    template_name = "order/cart/cart_items_v2.html"
    success_url = reverse_lazy("order:cart_items_v2")
    model = Cart

    def get_queryset(self):
        ''' get the user`s cart '''
        user_cart = self.model.objects.filter(customer = self.request.user.account, is_ordered = False)
        return user_cart

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        """ get the user`s cart """        
        context["carts"] = self.get_queryset()

        return context
        
        
    def get_form_kwargs(self):
        context = super().get_form_kwargs()

        # pass the queryset to get the cart of logged in user, use as basis for the form validation
        context['queryset'] = self.get_queryset()
                
        return context 
    
    def form_valid(self, form):
        ''' create an order instance and save the ordered cart instances with order '''
        
        instances = form.save(commit = False)
        
        # check if the customer id is in the season, if not get it and add to seassion
        customer_id = self.request.session.get("customer_id")
        
        if not customer_id :
            print("Not in seasson, creating")
            self.request.session["customer_id"] = self.request.user.account.id
            customer_id = self.request.session.get("customer_id")

        order = Order.objects.create(customer = customer.objects.get(id = customer_id))

        for instance in instances:
            instance.order_id = order
            instance.save() 
        
        return super().form_valid(form)
    

