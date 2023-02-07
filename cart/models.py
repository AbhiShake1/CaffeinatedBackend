from django.contrib.auth import get_user_model
from django.db import models

from product.models import Product


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    ordered = models.BooleanField(default=False)

    objects = models.Manager()

    def __str__(self):
        return f'{self.product.name}'
