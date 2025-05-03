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
from django.db.models import Sum, F, Exists, OuterRef, Value, Q
from account import views as account
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from common.views import LoginWithPermissionMixin
from common.mixin import FormResponseMixin
from transaction.models import *
from urllib.parse import urlencode
# Create your views here.



# admin view

class Index(LoginWithPermissionMixin, generic.TemplateView):
    template_name = "order/index.html"
    permission_required = ["Order.view_order", "Order.delete_order"]

class Get_unpaid_order(LoginWithPermissionMixin,generic.ListView):
    model = Order
    template_name = "order/unpaid_order_instances.html"
    context_object_name = "orders"
    permission_required = ["Order.view_order", "Order.delete_order"]
    
    status = "not paid"
    
    def get_queryset(self):
        ''' return all order that is not paid '''
        instances = self.model.objects.filter(status = self.status).annotate(total_price = Sum( F("cart_items__quantity") * F("cart_items__cake__price")), is_have_transactions = Exists( Transaction.objects.filter(order_id = OuterRef('pk')) ) ).order_by("-date_ordered")

        return instances

class Get_paid_order(Get_unpaid_order):
    template_name = "order/paid_order_instances.html"
    
    def get_queryset(self):
        ''' return all order that is paid '''
        instances = self.model.objects.filter(~Q(status = 'not paid'), ~Q(status = "delivered"), ~Q(status = "fully paid")).annotate(total_price = Sum( F("cart_items__quantity") * F("cart_items__cake__price")), is_have_transactions = Exists( Transaction.objects.filter(order_id = OuterRef('pk')) ) ).order_by("-date_ordered")

        return instances

class Get_delivered_order(Get_unpaid_order):
    status = 'delivered'
    template_name = "order/delivered_order_instances.html"
    
    def get_queryset(self):
        ''' return all order that are delivered and fully paid '''
        instances = self.model.objects.filter(Q(status = 'delivered') | Q(status = 'fully paid')).annotate(total_price = Sum( F("cart_items__quantity") * F("cart_items__cake__price")), is_have_transactions = Exists( Transaction.objects.filter(order_id = OuterRef('pk'), status = Status_choices.not_accepted) )).order_by("-date_ordered")

        return instances

class Status_form(FormResponseMixin, generic.UpdateView):
    form_class = ChangeStatusForm
    model = Order
    form_success_message = "Updated Status"
    template_name = "order/admin/change_status.html"

class Delete_order(LoginWithPermissionMixin, FormResponseMixin ,generic.DeleteView):
    template_name = "order/admin/order_delete.html"
    model = Order
    context_object_name = "order"
    permission_required = ["order.delete_order"]
    form_success_message = "Deleted Order"
    
    def get_queryset(self):
        return self.model.objects.prefetch_related("cart_items__cake").all()

 

    


# customer view 

class CakeDetailMixin(SingleObjectMixin):
    model = Cake
    
    def get_object(self, queryset=None):
        #Fetch the specific Cake that the user is adding to the cart.
        return get_object_or_404(Cake, pk=self.kwargs["pk"])  # Get Cake from URL
    
class Cart_Created(generic.TemplateView):
    template_name = "order/cart/created_cart.html"

# make sure that only authenticated users can access this view
class Cart_form(account.CustomerPermission, CakeDetailMixin, generic.CreateView):
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

# not used 
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
        user_cart = self.model.objects.annotate(total_price=Sum( F("cake__price") * F("quantity") )).filter(customer = self.request.user.account, is_ordered = False)

        
        return user_cart

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        """ get the user`s cart """        
        context["carts"] = self.queryset_cache

        return context
        
        
    def get_form_kwargs(self):
        context = super().get_form_kwargs()

        # pass the queryset to get the cart of logged in user, use as basis for the form validation
        context['queryset'] = self.get_queryset()
        
        # save it to a variable to avoid refetching
        self.queryset_cache = context["queryset"]
                
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
    

class Customer_orders(generic.TemplateView):
    template_name = "order/customer_order/index.html"

class Customer_orders_pending(generic.ListView):
    template_name = "order/customer_order/pending_order_table.html"
    model = Order
    context_object_name = "orders"

    def get_status(self):
        return Q(status = "not paid")
    
    def get_queryset(self):
        ''' return the orders that are specific to current logged in customer '''
        user_orders = self.model.objects.filter(self.get_status() ,customer = self.request.user.account)\
                      .annotate(total_price = Sum( F("cart_items__quantity") * F("cart_items__cake__price"))).order_by("-date_ordered")

        return user_orders

class Customer_orders_on_progress(Customer_orders_pending):
    
    template_name = "order/customer_order/onprogress_order.html"
    def get_status(self):
        ''' 
            Pending orders are status that are not the status of not paid, delivered, and fully paid
        '''
        return ~Q(status = "not paid") & ~Q(status = "delivered") & ~Q(status = "fully paid")

class Customer_orders_delivered(Customer_orders_pending):
    
    def get_status(self):
        ''' 
            are status are delivered and fully paid
        '''
        return Q(status = "delivered") | Q(status = "fully paid") 