from django.db import models
from customer.models import *
from cake.models import *
from account import views as account
from datetime import date, timedelta


class Cart(models.Model):
    customer = models.ForeignKey(customer, related_name="cart_items", on_delete=models.CASCADE)
    cake = models.ForeignKey(Cake, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    
    order_id = models.ForeignKey("Order", related_name= "cart_items", on_delete=models.SET_NULL, null=True, blank=True, default=None) 
    is_ordered = models.BooleanField(default=False)
    
    date_added = models.DateTimeField(auto_now_add=True)    
    
    
    def __str__(self):
        return f"{self.customer}`s {self.cake}" 

class Order(models.Model):
    
    status_choices = (
        ("not paid", "not paid"),
        ("paid", "paid"),
        ("in progress", "in progress"),
        ("halfway", "halfway"),
        ("almost finished", "almost finished"),
        ("finished", "finished"),
        ("delivered", "delivered"),
        ("fully paid", "fully paid")
    )
    
    customer = models.ForeignKey(customer, related_name="orders", on_delete=models.CASCADE)
    
    status = models.CharField(choices=status_choices, max_length=15, default="not paid")
    
    delivery_date = models.DateField(default=date.today() + timedelta(days=7)) 
    date_ordered = models.DateTimeField(auto_now_add=True)    
    
    def __str__(self):
        return f"{self.customer}`s order {self.id}" 
    