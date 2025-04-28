from django.db import models
from order.models import Order
# Create your models here.


class Status_choices(models.IntegerChoices):
    not_accepted = 0, 'not_accepted'
    accepted = 1, 'accepted'

class Type_choices(models.IntegerChoices):
    partial = 0, 'partial payment'
    full = 1, 'full payment'


class Transaction(models.Model):

    order_id = models.ForeignKey("order.Order", related_name="transactions" ,on_delete=models.CASCADE)
    image_prof = models.ImageField(upload_to="Transactions/images/")
    reference_number = models.CharField(max_length=15)
    amount = models.IntegerField()
    status = models.IntegerField(choices=Status_choices, default=0)
    payment_type = models.IntegerField(choices=Type_choices, default=0)
    date_submitted = models.DateTimeField(auto_now_add=True)  