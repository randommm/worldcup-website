from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True)
    data = models.CharField(max_length=20000, default="xx")

    def __str__(self):
        return str(self.user)
