from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Message(models.Model):
    message = models.TextField()
    sender = models.ForeignKey(User, null=True, related_name='sent_messages' , on_delete=models.SET_NULL)
    receiver = models.ForeignKey(User, null=True, related_name='received_messages' , on_delete=models.SET_NULL)
    created_at = models.DateField()
    
    