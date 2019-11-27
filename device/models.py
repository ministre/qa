from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Interface(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class CustomField(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class DeviceType(models.Model):
    tag = models.CharField(max_length=100)
    desc = models.CharField(max_length=1000)
    desc_genitive = models.CharField(max_length=1000, null=True, blank=True)
    cf = models.ManyToManyField(CustomField, related_name='custom_fields', blank=True)
    ifaces = models.ManyToManyField(Interface, related_name='interfaces', blank=True)
    redmine_url = models.CharField(max_length=1000, blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='device_type_created_by', on_delete=models.CASCADE,
                                   blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='device_type_updated_by', on_delete=models.CASCADE,
                                   blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.desc


class Vendor(models.Model):
    name = models.CharField(max_length=400)
    created_by = models.ForeignKey(User, related_name='vendor_created_by', on_delete=models.CASCADE,
                                   blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='vendor_updated_by', on_delete=models.CASCADE,
                                   blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.name


class Device(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    model = models.CharField(max_length=400)
    hw = models.CharField(max_length=100)
    type = models.ForeignKey(DeviceType, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='device_created_by', on_delete=models.CASCADE,
                                   blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='device_updated_by', on_delete=models.CASCADE,
                                   blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.model


class CustomValue(models.Model):
    value = models.CharField(max_length=1000)
    field = models.ForeignKey(CustomField, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)

    def __str__(self):
        return self.value


class DevicePhoto(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="device/")
    desc = models.CharField(max_length=500)


class Button(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Led(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class DeviceInterface(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    interface = models.ForeignKey(Interface, on_delete=models.CASCADE)
    quantity = models.IntegerField()
