from django.db import models
from django.contrib.auth.models import User

# choices

gender_choices = ( 
    ("Male", "Male"),
    ("Female", "Female"),
    ("Prefer not to say", "Prefer not to say")
)

class customer(models.Model):
    first_name = models.CharField(max_length=50)
    init_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_num = models.CharField(max_length=11)
    home_address = models.CharField(max_length=100, default="Daraga")
    email_add = models.EmailField(max_length=254)
    contact_num = models.IntegerField(default="09123456789")
    gender = models.CharField(
         max_length=50,
         choices = gender_choices
        )
    profile_pic = models.ImageField(upload_to="Customer/Profile Picture", null=True, blank=True)

    def __str__(self):
        return self.firstname
