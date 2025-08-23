from django.db import models
from django_resized import ResizedImageField

class Car(models.Model):
    CONDITION_CHOICES = [
        ('new', 'Brand New'),
        ('used', 'Pre-Owned'),
    ]
    
    TRANSMISSION_CHOICES = [
        ('automatic', 'Automatic'),
        ('manual', 'Manual'),
    ]
    
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    mileage = models.PositiveIntegerField(null=True, blank=True)
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    description = models.TextField()
    featured = models.BooleanField(default=False)
    sold = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.year} {self.make} {self.model}"

class CarImage(models.Model):
    car = models.ForeignKey(Car, related_name='images', on_delete=models.CASCADE)
    image = ResizedImageField(size=[800, 600], quality=85, upload_to='car_images/')
    is_main = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)  # Add this line
    
    class Meta:
        ordering = ['order']  # Add default ordering
        
    def __str__(self):
        return f"Image for {self.car}"