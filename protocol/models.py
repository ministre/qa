from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from device.models import Device, Sample, Firmware
from testplan.models import Testplan, Test


class Resolution(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Protocol(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    testplan = models.ForeignKey(Testplan, on_delete=models.CASCADE)
    # firmware = models.ForeignKey(Firmware, on_delete=models.CASCADE)
    started = models.DateField(default=datetime.now, blank=True)
    completed = models.DateField(blank=True, null=True)
    status = models.ForeignKey(Resolution, on_delete=models.CASCADE, blank=True, null=True)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE, blank=True, null=True)
    scan = models.FileField(upload_to="protocol/files/", blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='protocol_c', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='protocol_u', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)


class TestResult(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    protocol = models.ForeignKey(Protocol, on_delete=models.CASCADE)
    result = models.IntegerField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='result_u', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)
