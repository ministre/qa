from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from device.models import Device


class DocumType(models.Model):
    name = models.CharField(max_length=300)
    created_by = models.ForeignKey(User, related_name='documtype_created_by_user', on_delete=models.CASCADE,
                                   blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='documtype_updated_by_user', on_delete=models.CASCADE,
                                   blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.name


class Docum(models.Model):
    name = models.CharField(max_length=300, blank=True, null=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    type = models.ForeignKey(DocumType, on_delete=models.CASCADE)
    file = models.FileField(upload_to="docum/files/")
    created_by = models.ForeignKey(User, related_name='docum_created_by_user', on_delete=models.CASCADE,
                                   blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='docum_updated_by_user', on_delete=models.CASCADE,
                                   blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)
