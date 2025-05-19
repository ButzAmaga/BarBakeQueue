from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Transaction, Status_choices, Type_choices
from order.models import Order
from .forms import TransactionForm
from django.urls import reverse_lazy
from django.contrib import messages
from common.views import LoginWithPermissionMixin
import csv
from django.http import HttpResponse
from django.db.models import Sum, F
from customer.models import customer

# Create your views here.

# customer order transaction form
class Customer_form(LoginWithPermissionMixin, generic.CreateView):
    model = Transaction
    template_name = "transaction/customer_form.html"
    form_class = TransactionForm
    success_url = reverse_lazy("transaction:customer_form")
    permission_required = ["transaction.add_transaction"]
    permission_denied_message = "You dont have the permission"
    # set up the initial value or order id of the form

    def get_success_url(self):
        return reverse_lazy("transaction:customer_form", kwargs={'order_id': self.kwargs.get('order_id')})
    
    def get_form_kwargs(self):
        '''
            Get the order object for the transaction and place it as kwargs for the form, raise 404 if the order 
            is not found
        ''' 
        data = super().get_form_kwargs()
        #data["order_id"] = get_object_or_404(Order, id = self.kwargs.get("order_id", None))
        data["order_id"] = Order.objects.annotate(total_price = Sum( F("cart_items__quantity") * F("cart_items__cake__price"))).get(id = self.kwargs.get("order_id"))
        
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
   
   
   
   
# Admin 

class Order_transactions(LoginWithPermissionMixin, generic.ListView):
    model = Transaction
    context_object_name = "transactions"
    template_name = "transaction/admin/order_transaction.html"
    permission_required = ["transaction.view_transaction"]
    
    def get_queryset(self):
        """ 
            return the transactions associated with this order id
        """
        transactions = self.model.objects.filter(order_id = self.kwargs["order_id"], status = Status_choices.not_accepted)    
        return transactions
    
class Accept_transaction(LoginWithPermissionMixin, generic.RedirectView):

    permission_required = ["transaction.change_transaction"]
    query_string = True
    pattern_name = "common:form_response"

    
    def get_redirect_url(self, *args, **kwargs):
        print("Test")
        """ 
            accept the transaction and then update the status of the order
        """
        
        transaction = get_object_or_404(Transaction, pk = kwargs["pk"])
        transaction.status = Status_choices.accepted
            
        # get the order_jd instance 
        order_id = transaction.order_id
        
        if order_id.status == "delivered":
            # if order instance is already delivered then the current transaction is for full payment and the order instance 
            # status should be fully paid
            transaction.payment_type = Type_choices.full
            order_id.status = "fully paid"
            order_id.save()
        else:
            # update the order status, byu default transaction type is partial
            order_id.status = "paid"
            order_id.save()
        
        
             
        # save the changes
        transaction.save()
        
        kwargs.pop("pk")
        
        return super().get_redirect_url(*args, **kwargs) 
 

class TransactionList(LoginWithPermissionMixin, generic.ListView):
    model = Transaction
    template_name = "transaction/admin/index.html"
    context_object_name = "transactions"
    paginate_by = 10
    permission_required = ["transaction.view_transaction"]

    def get_queryset(self):
        return self.model.objects.all().filter(status = 1).order_by("-date_submitted")
    
  
class TransactionDetail(LoginWithPermissionMixin, generic.DetailView):
    model = Transaction
    template_name = "transaction/admin/transaction_detail.html"
    context_object_name = "transaction"
    permission_required = ["transaction.view_transaction"]
    

    
def export_transaction_to_csv(request):
    # Create the HttpResponse object with CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="yourmodel.csv"'

    writer = csv.writer(response)
    # Write the header row (field names)
    writer.writerow(['Order Id', 'Name and order id', 'Image Prof', 'Reference Number', 'Amount', 'Status ( 0 - not_accepted | 1 - accepted )', 'Payment Type (0 - partial | 1 - full)', 'Date Submitted'])  # replace with your field names
    
    # Get model field names
    field_names = [field.name for field in Transaction._meta.get_fields() if not field.many_to_many and not field.one_to_many]

    # Write data rows
    for instance in Transaction.objects.all():
        writer.writerow([getattr(instance, field) for field in field_names])

    return response
 