from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Message(models.Model):
    
    user = models.ForeignKey(User, null=True, related_name='messages' , on_delete=models.CASCADE)
    message = models.TextField()
    is_channel_sender = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    
    
    