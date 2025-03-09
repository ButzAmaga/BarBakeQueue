from django.db import models
from customer.models import *
from cake.models import *



class Cart(models.Model):
    customer = models.ForeignKey(customer, related_name="cart_items", on_delete=models.CASCADE)
    cake = models.ForeignKey(Cake, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    
    order_id = models.ForeignKey("Order", on_delete=models.DO_NOTHING, null=True, blank=True, default=None) 
    is_ordered = models.BooleanField(default=False)
    
    date_added = models.DateTimeField(auto_now_add=True)    
    
    
    def __str__(self):
        return f"{self.customer}`s {self.cake}" 

class Order(models.Model):
    customer = models.ForeignKey(customer, related_name="orders", on_delete=models.CASCADE)
    
    date_ordered = models.DateTimeField(auto_now_add=True)    
    
    def __str__(self):
        return f"{self.customer}`s order {self.id}" 
    