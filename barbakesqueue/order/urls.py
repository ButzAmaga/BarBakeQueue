from django.urls import path, include
from .views import * 

app_name = 'order'

urlpatterns = [
    path('customize/', Cart_form.as_view(), name='cart_form'), # customize cart
    
] 
