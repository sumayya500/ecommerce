from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class CustomUser(AbstractUser):

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    verification_code = models.UUIDField(default=uuid.uuid4, editable=False)
    wallet = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

