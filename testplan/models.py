from django.db import models
from device.models import DeviceType
from django.contrib.auth.models import User
from datetime import datetime


class Checklist(models.Model):
    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Checklists"


class Testplan(models.Model):
    name = models.CharField(max_length=1000)
    version = models.CharField(max_length=300)
    device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(User, related_name='testplan_created_by_user', on_delete=models.CASCADE,
                                   blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='testplan_updated_by_user', on_delete=models.CASCADE,
                                   blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)
    redmine_url = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.name


class Chapter(models.Model):
    testplan = models.ForeignKey(Testplan, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    text = models.TextField(max_length=100000)
    redmine_url = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Chapters"


class Category(models.Model):
    name = models.CharField(max_length=1000)
    testplan = models.ForeignKey(Testplan, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Test(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    purpose = models.TextField(max_length=5000, null=True, blank=True)
    procedure = models.TextField(null=True, blank=True)
    expected = models.TextField(null=True, blank=True)
    redmine_url = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.name
