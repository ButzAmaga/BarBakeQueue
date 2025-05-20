from django.urls import path, include
from .views import * 
from account.views import Customer_registration
app_name = 'main'

urlpatterns = [
    path('', Index_page.as_view(), name='index'), # index page
    path('whats_new', Index_whats_new.as_view(), name='index_whats_new'), # index page
    
    
    path('cakes/', Cake_page.as_view(), name='cake_page'), # cake customer page
    path('register', Customer_registration.as_view(), name='customer_register'), # customer registration page
    
] 
