from django.contrib.auth import get_user_model
from django.db import models
from pyfcm import FCMNotification

from CaffeinatedBackend import settings


# Create your models here.
class Notification(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.send_push_notification()

    def send_push_notification(self):
        push_service = FCMNotification(api_key=settings.FCM_SERVER_KEY)
        registration_id = self.user.fcm_token
        if registration_id:
            message_title = self.title
            message_body = self.description
            sound = f'slow_spring_board.mp3'
            push_service.notify_single_device(
                registration_id=registration_id,
                message_title=message_title,
                message_body=message_body,
                sound=sound,
            )
