from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Tier(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.name) + "" + str(self.description)


class Image(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    upload = models.ImageField(upload_to='uploads/')
