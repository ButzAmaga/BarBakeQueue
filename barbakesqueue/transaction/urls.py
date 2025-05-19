from django.urls import path, include
from .views import * 

app_name = 'transaction'

urlpatterns = [
    # customer 
    path('customer/<int:order_id>', Customer_form.as_view(), name='customer_form'), # customer order transaction form    
    
    # admin
    path('order/transaction/list', TransactionList.as_view(), name='transaction_list'), 


    path('order/transaction/<int:order_id>', Order_transactions.as_view(), name='order_transactions'), # order transaction    
    path('order/transaction/<pk>/accept', Accept_transaction.as_view(), name='accept_transaction'), # accept transaction
    
    # csv 
    path('order/transaction/get/csv', export_transaction_to_csv, name='transaction_csv'), # download the transaction csv
] 


