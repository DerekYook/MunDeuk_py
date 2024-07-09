from django.db import models


# Create your models here.
class UserList(models.Model):
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    group = models.CharField(max_length=100)

    def __str__(self):
        return self.username
