from django.urls import path, include
from .views import * 

app_name = 'order'

urlpatterns = [
    path('cart/customize/<pk>', Cart_form.as_view(), name='cart_form'), # customize cart
    path('cart/cart_added/', Cart_Created.as_view(), name='cart_created'), # success message for creating the cart
    path('cart/cart_items', Cart_items.as_view(), name='cart_items'), # cart items for the current user
    
] 
