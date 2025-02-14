import uuid, random
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
# Address book user - each user that logs into the application
class ABUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=20)

def generate_random_color():
    """Generate a random hex color."""
    colors = ["#FF5733", "#33FF57", "#3357FF", "#FF33A1", "#FFD700", "#FF69B4", "#ffbfbf", "#cdfa2a", "#11e3fa", "#8611fa"]
    return random.choice(colors)

# Tag - allows multiple tags to be associated with a contact
class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(ABUser, on_delete=models.CASCADE, related_name="tags")
    color = models.CharField(max_length=7, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.color:
            self.color = generate_random_color()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# Contact - associated with ABUser's addr_bk_id
class Contact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    addr_bk_id = models.ForeignKey(ABUser, on_delete=models.CASCADE, related_name="contacts")
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email_address = models.EmailField(max_length=255,null=True, blank=True)
    phone_number = models.CharField(max_length=20,null=True, blank=True)
    postcode = models.CharField(max_length=10,null=True, blank=True)
    date_added = models.DateTimeField(default=timezone.now)

    # Many-to-Many relationship with Tag
    tags = models.ManyToManyField(Tag, blank=True, related_name="contacts")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"