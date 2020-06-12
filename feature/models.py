from django.db import models
from device.models import DeviceType
from django.contrib.auth.models import User
from datetime import datetime


class FeatureList(models.Model):
    device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    version = models.CharField(max_length=300)
    created_by = models.ForeignKey(User, related_name='fl_c', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='fl_u', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)
    redmine_wiki = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.name

    def update_timestamp(self, user):
        self.updated_by = user
        self.updated_at = datetime.now()
        self.save()
        return True


class FeatureListCategory(models.Model):
    feature_list = models.ForeignKey(FeatureList, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Feature List Categories"


class FeatureListItem(models.Model):
    category = models.ForeignKey(FeatureListCategory, related_name='category_item', on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    optional = models.BooleanField(blank=True, null=True, default=False)
    created_by = models.ForeignKey(User, related_name='fli_c', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='fli_u', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)
