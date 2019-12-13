from django.db import models
from device.models import DeviceType
from django.contrib.auth.models import User
from datetime import datetime


class FeatureList(models.Model):
    device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=1000)
    version = models.CharField(max_length=300)
    created_by = models.ForeignKey(User, related_name='feature_list_created_by', on_delete=models.CASCADE,
                                   blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='feature_list_updated_by', on_delete=models.CASCADE,
                                   blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)
    redmine_url = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.name


class FeatureListCategory(models.Model):
    feature_list = models.ForeignKey(FeatureList, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Feature List Categories"
