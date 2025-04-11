from django.urls import path, include
from .views import * 

app_name = 'order'

urlpatterns = [
    path('orders/', Index.as_view(), name='orders'), # list of orders
    path('orders/get/not_paid', Get_unpaid_order.as_view(), name='not_paid'), # list of unpaid order
    path('orders/delete/<pk>', Delete_order.as_view(), name='delete_order'), # list of unpaid order
    
     
    path('cart/customer/customize/<pk>', Cart_form.as_view(), name='cart_form'), # customize cart
    path('cart/customer/cart_added/', Cart_Created.as_view(), name='cart_created'), # success message for creating the cart
    path('cart/customer/v2/cart_items/', Cart_items_v2.as_view(), name='cart_items_v2'), # cart items for the current user
    path('order/customer/orders', Customer_orders.as_view(), name='customer_orders'), # main order interface for the customer user
    path('order/customer/orders/pending', Customer_orders_pending.as_view(), name='customer_orders_pending'), # pending order interface for the customer user
] 
