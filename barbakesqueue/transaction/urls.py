from django.urls import path, include
from .views import * 

app_name = 'transaction'

urlpatterns = [
    path('customer/<int:order_id>', Customer_form.as_view(), name='customer_form'), # customer order transaction form    
] 
