from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class CustomField(models.Model):
    name = models.CharField(max_length=500)
    desc = models.CharField(max_length=1000, blank=True, null=True)
    type = models.CharField(max_length=10, default='Text')
    created_by = models.ForeignKey(User, related_name='field_c', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='field_u', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.name


class CustomFieldItem(models.Model):
    name = models.CharField(max_length=1000)
    custom_field = models.ForeignKey(CustomField, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='item_c', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='item_u', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.name


class DeviceType(models.Model):
    tag = models.CharField(max_length=100)
    desc = models.CharField(max_length=1000)
    desc_genitive = models.CharField(max_length=1000, null=True, blank=True)
    cf = models.ManyToManyField(CustomField, related_name='custom_fields', blank=True)
    redmine_project = models.CharField(max_length=1000, blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='type_c', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='type_u', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.desc

    class Meta:
        ordering = ('desc',)


class Vendor(models.Model):
    name = models.CharField(max_length=400)
    created_by = models.ForeignKey(User, related_name='vendor_c', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='vendor_u', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.name


class Device(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    model = models.CharField(max_length=400)
    hw = models.CharField(max_length=100)
    type = models.ForeignKey(DeviceType, on_delete=models.CASCADE)
    redmine_project = models.CharField(max_length=1000, blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='device_c', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='device_u', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.model


class CustomValue(models.Model):
    field = models.ForeignKey(CustomField, on_delete=models.CASCADE)
    item = models.ForeignKey(CustomFieldItem, on_delete=models.CASCADE, blank=True, null=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    value = models.CharField(max_length=1000, blank=True, null=True)


class DevicePhoto(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="device/")
    desc = models.CharField(max_length=500)
    created_by = models.ForeignKey(User, related_name='photo_c', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='photo_u', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)


class Sample(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    sn = models.CharField(max_length=50)
    desc = models.CharField(max_length=1000, blank=True, null=True)
    user_login = models.CharField(max_length=100, blank=True, null=True)
    user_password = models.CharField(max_length=100, blank=True, null=True)
    support_login = models.CharField(max_length=100, blank=True, null=True)
    support_password = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='sample_c', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='sample_u', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.sn
