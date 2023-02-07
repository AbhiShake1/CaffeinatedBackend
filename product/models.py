from django.db import models
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from consumer.models import Consumer


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    available = models.BooleanField(default=True)
    bookmarked_by = models.ManyToManyField(Consumer, related_name='bookmarked_products', blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5)
    image = models.ImageField(upload_to='products/', default='products/default.png')
    image_url = models.URLField(null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Check if the image field has changed
        if self.image and not hasattr(self, '_file_uploaded'):
            # Build the Drive API client
            service = build('drive', 'v3')

            # Create the file metadata
            file_metadata = {'name': self.image.name}

            # Upload the file
            media = MediaFileUpload(self.image.path, mimetype='image/jpeg')
            file = service.files().create(body=file_metadata, media_body=media,
                                          fields='id').execute()
            file_id = file.get('id')

            permission = {
                'type': 'anyone',
                'role': 'reader',
            }
            service.permissions().create(fileId=file_id, body=permission, fields='id').execute()

            # Get the file URL
            self.image_url = f"https://drive.google.com/u/0/uc?id={file_id}"

            self._file_uploaded = True

        super().save(*args, **kwargs)
