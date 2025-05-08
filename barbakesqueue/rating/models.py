from django.db import models
from customer.models import *
from cake.models import *
# Create your models here.


class Rating_rate_choices(models.IntegerChoices):
    one = 1, "Very Dissatisfied"
    two = 2, "Dissatisfied"
    three = 3, "Neutral or Average"
    four = 4, "Satisfied"
    five = 5, "Very Satisfied"
    
class Rating(models.Model):
    customer = models.ForeignKey(customer, related_name='ratings', on_delete=models.CASCADE)
    cake = models.ForeignKey(Cake, related_name='ratings', on_delete=models.CASCADE)
    
    rate = models.IntegerField(choices=Rating_rate_choices, default=1)
    comment = models.TextField()

    def __str__(self):
        return f"{self.customer}`s {self.cake} => {self.rate}"
    
    