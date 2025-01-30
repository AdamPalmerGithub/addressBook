import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class ABUser(AbstractUser):
    userid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email_address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
