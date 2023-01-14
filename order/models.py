from django.db import models
from pyfcm import FCMNotification

from CaffeinatedBackend import settings
from product.models import Product


# Create your models here.
class Order(models.Model):
    PENDING = 'pending'
    DONE = 'done'

    ORDER_STATUS = (
        (PENDING, 'Pending'),
        (DONE, 'Done'),
    )

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default=PENDING)
    items = models.ManyToManyField(Product)

    objects = models.Manager()

    def send_push_notification(self):
        push_service = FCMNotification(api_key=settings.FCM_SERVER_KEY)
        try:
            registration_id = self.student.userprofile.fcm_token
        except:
            registration_id = None
        if registration_id:
            message_title = "Order Status Update"
            message_body = f"Your order status has been updated to {self.status}"
            result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title,
                                                       message_body=message_body)
            return result
        else:
            return None

    def save(self, *args, **kwargs):
        if self.pk:
            orig = Order.objects.get(pk=self.pk)
            if orig.status != self.status:
                self.send_push_notification()
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.items} for {self.student}'
