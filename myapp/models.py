import uuid
from django.db import models

# Create your models here.
class User(models.Model):
    userid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=50)
    number = models.CharField(max_length=20)
    email = models.CharField(max_length=40)
