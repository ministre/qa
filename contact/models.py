from django.db import models
from django.contrib.auth.models import User
from device.models import Vendor
from datetime import datetime


class Contact(models.Model):
    surname = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, blank=True, null=True)
    post = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    vendor = models.ForeignKey(Vendor, related_name='contact_vendor', on_delete=models.CASCADE, blank=True, null=True)
    username = models.ForeignKey(User, related_name='contact_username', on_delete=models.CASCADE, blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='contact_c', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='contact_u', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        order_with_respect_to = 'surname'

    def __str__(self):
        full_name = str(self.surname) + ' ' + str(self.name)
        if self.patronymic:
            full_name += ' ' + str(self.patronymic)
        return full_name
