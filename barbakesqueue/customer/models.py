from django.db import models
from django.contrib.auth.models import User

# choices

gender_choices = ( 
    ("Male", "Male"),
    ("Female", "Female"),
    ("Prefer not to say", "Prefer not to say")
)

class customer(models.Model):

    account = models.OneToOneField(User, related_name='account' , on_delete=models.CASCADE, null=True)
    
    first_name = models.CharField(max_length=50)
    init_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_num = models.CharField(max_length=11)
    home_address = models.CharField(max_length=100, default="Daraga")
    email_address = models.EmailField(max_length=254)
    
    gender = models.CharField(
         max_length=50,
         choices = gender_choices
        )
    
    profile_pic = models.ImageField(upload_to="Customer/Profile Picture")

    def __str__(self):
        return f'{self.first_name} {self.init_name} {self.last_name}'
