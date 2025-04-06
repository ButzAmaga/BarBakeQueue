from django.db import models
from order.models import Order
# Create your models here.
class Transaction(models.Model):
    order_id = models.ForeignKey("order.Order", related_name="transactions" ,on_delete=models.CASCADE)
    image_prof = models.ImageField(upload_to="Transactions/images/")
    reference_number = models.CharField(max_length=15)
    amount = models.IntegerField()
    date_submitted = models.DateTimeField(auto_now_add=True)  