from django.db import models
from customer.models import *
from cake.models import *



class Cart(models.Model):
    customer = models.ForeignKey(customer, related_name="cart_items", on_delete=models.CASCADE)
    cake = models.ForeignKey(Cake, on_delete=models.CASCADE)
    
    quantity = models.IntegerField()
    
    date_added = models.DateTimeField(auto_now_add=True)    
    