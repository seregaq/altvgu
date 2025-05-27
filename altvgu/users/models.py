from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    photo = models.ImageField(upload_to='users/', blank=True, null=True)
    date_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username
