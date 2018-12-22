from django.db import models


class DeviceType(models.Model):
    tag = models.CharField(max_length=100)
    desc = models.CharField(max_length=300)


class CustomField(models.Model):
    name = models.CharField(max_length=500)
