from django.urls import path, include
from .views import * 

app_name = 'transaction'

urlpatterns = [
    # customer 
    path('customer/<int:order_id>', Customer_form.as_view(), name='customer_form'), # customer order transaction form    
    
    # admin
    path('order/transaction/<int:order_id>', Order_transactions.as_view(), name='order_transactions'), # order transaction    
] 
