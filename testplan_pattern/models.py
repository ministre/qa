from django.db import models
from device.models import DeviceType
from django.contrib.auth.models import User
from datetime import datetime


class Pattern(models.Model):
    name = models.CharField(max_length=1000)
    types = models.ManyToManyField(DeviceType, related_name='device_types', blank=True)
    redmine_url = models.CharField(max_length=1000, blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='pattern_created', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='pattern_updated', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)
