import uuid

from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
# Address book user - each user that logs into the application
class ABUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=20)
# Contact - associated with ABUser's addr_bk_id
class Contact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    addr_bk_id = models.ForeignKey(ABUser, on_delete=models.CASCADE, related_name="contacts")
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email_address = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=20)
    postcode = models.CharField(max_length=10)
    date_added = models.DateTimeField(default=timezone.now)
