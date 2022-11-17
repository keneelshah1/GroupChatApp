from django.db import models
from datetime import datetime

# Create your models here.


class UserData(models.Model):
    username = models.CharField(max_length=255, unique=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    profilepic = models.ImageField(blank=True, upload_to='images')

    def __str__(self):
        return self.username



class Tasks(models.Model):
    task_categories = [('AC', 'Active'), ('CO', 'Completed')]
    username = models.ForeignKey(UserData, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=255)
    task_status = models.CharField(max_length=2, choices=task_categories, default='AC')


