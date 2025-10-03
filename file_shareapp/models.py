# myapp/models.py
from django.db import models
import uuid

from django.conf import settings

class File(models.Model):
    id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        null=True
    )
    title = models.CharField(max_length=200)
    uploaded_file = models.FileField(upload_to='uploads/')
    expiry_date = models.DateField(null=False, blank=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title