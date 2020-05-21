from django.db import models
from django.contrib.auth.models import User

class User_Profile(models.Model):
    users = models.OneToOneField(User, on_delete = models.CASCADE)
    bio = models.CharField('bio', max_length = 100, default = "Please add a profile.")

    def __str__(self):
        return self.users.username