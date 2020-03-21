from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from device.models import Device
from testplan.models import Testplan
from firmware.models import Firmware


class Resolution(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Protocol(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    testplan = models.ForeignKey(Testplan, on_delete=models.CASCADE)
    firmware = models.ForeignKey(Firmware, on_delete=models.CASCADE)
    started = models.DateField(default=datetime.now, blank=True)
    completed = models.DateField(blank=True, null=True)
    status = models.ForeignKey(Resolution, on_delete=models.CASCADE, blank=True, null=True)
    scan = models.FileField(upload_to="protocol/files/", blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='protocol_c', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='protocol_u', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)