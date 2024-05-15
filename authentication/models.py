from django.db import models

class UsersTab(models.Model):
    uniqueId=models.CharField(max_length=255)
    name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    phone=models.CharField(max_length=10)


class UsersWatchList(models.Model):
    uniqueId=models.CharField(max_length=255)
    symbol=models.CharField(max_length=255)


