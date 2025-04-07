from django.urls import path, include
from .views import * 
from account.views import Customer_registration
app_name = 'main'

urlpatterns = [
    path('', Cake_page.as_view(), name='cake_page'), # cake customer page
    path('register', Customer_registration.as_view(), name='customer_register'), # customer registration page
    
] 
