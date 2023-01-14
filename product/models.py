from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    available = models.BooleanField(default=True)

    objects = models.Manager()

    def __str__(self):
        return self.name
