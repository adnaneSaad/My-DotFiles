from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class StudentData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Marks = models.JSONField(default=dict, blank=True)
    Results = models.JSONField(default=dict, blank=True)
    Audio = models.FileField(upload_to='audio/', null=True, blank=True)
    history = models.JSONField(default=list, blank=True)


    def __str__(self):
        return f"StudentData ({self.user.username})"