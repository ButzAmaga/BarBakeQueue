from django.db import models

class Shape(models.Model):
    shape = models.CharField(max_length=50)
    image = models.ImageField(upload_to="Cakes/Shape")
    cake_id = models.ForeignKey("Cake", on_delete=models.CASCADE)   

class Size(models.Model):
    name = models.CharField(max_length=100)
    add_price = models.IntegerField()
    cake_id = models.ForeignKey("Cake", on_delete=models.CASCADE)


class Layer(models.Model):
    num_layer = models.IntegerField()
    add_price = models.IntegerField()
    cake_id = models.ForeignKey("Cake", on_delete=models.CASCADE)


class Filling(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="Cakes/Filling")
    add_price = models.IntegerField()
    cake_id = models.ForeignKey("Cake", on_delete=models.CASCADE)

class Cake_image(models.Model):
    image = models.ImageField(upload_to="Cakes")
    cake_id = models.ForeignKey("Cake", on_delete=models.CASCADE)    

class Cake(models.Model):
    AVAILABILITY_CHOICES = [
        ('available', 'Available'),
        ('not_available', 'Not Available'),
    ]

    OCCASION_CHOICES = [
        ('birthday', 'Birthday'),
        ('wedding', 'Wedding'),
        ('anniversary', 'Anniversary'),
        ('monthsary', 'Monthsary'),
        ('christening', 'Christening'),
        ('debut', 'Debut'),
        ('gender_reveal', 'Gender Reveal'),
        ('christmas', 'Christmas'),
        ('new_year', 'New Year'),
    ]

     # Other fields

    price = models.IntegerField()
    caketype = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
   #layer = models.ManyToManyField('Layer')
    flavor = models.CharField(max_length=100)
   #filling = models.ManyToManyField('Filling')
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES)
    group_by = models.CharField(max_length=20, choices=OCCASION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name