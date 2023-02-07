from django.contrib.auth import get_user_model
from django.db import models

from cart.models import Cart
from notification.models import Notification


# Create your models here.
class Order(models.Model):
    PENDING = 'pending'
    DONE = 'done'
    CANCELLED = 'cancelled'

    ORDER_STATUS = (
        (PENDING, 'Pending'),
        (DONE, 'Done'),
        (CANCELLED, 'Cancelled'),
    )

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    carts = models.ManyToManyField(Cart, related_name='orders')
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default=PENDING)

    objects = models.Manager()

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        self.create_notification(is_new)

    def create_notification(self, is_new):
        if is_new:
            Notification.objects.create(
                user=self.user,
                title='Your order has been placed.',
                description='It should be ready shortly',
            )
        else:
            if self.status == self.DONE:
                Notification.objects.create(
                    user=self.user,
                    title='Your order is completed',
                    description='Pick it up!',
                )
            elif self.status == self.CANCELLED:
                Notification.objects.create(
                    user=self.user,
                    title='Your order has been cancelled',
                    description='We apologize for the inconvenience',
                )

    def __str__(self):
        cart_products = [cart.product.name for cart in self.carts.all()]
        return f'{", ".join(cart_products)} for {self.user.name}'
