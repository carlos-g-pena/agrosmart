from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils.timezone import now

class CustomUser(AbstractUser):
    pass

class Product(models.Model):
    name = models.CharField(max_length=255)
    weight = models.FloatField()  
    date_added = models.DateTimeField(default=now)  
    registered_by = models.ForeignKey(settings.AUTH_USER_MODEL,  
        on_delete=models.CASCADE) 

    def __str__(self):
        return self.name