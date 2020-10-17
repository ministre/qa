from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from testplan.models import Testplan, Test
from device.models import Device, Firmware, DeviceSample


class Branch(models.Model):
    name = models.CharField(max_length=300)
    created_by = models.ForeignKey(User, related_name='branch_c', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, related_name='branch_u', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Protocol(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.RESTRICT)
    testplan = models.ForeignKey(Testplan, on_delete=models.CASCADE, blank=True, null=True)
    started = models.DateField(default=timezone.now)
    completed = models.DateField(blank=True, null=True)
    status = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, related_name='protocol_c', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, related_name='protocol_u', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(default=timezone.now)


class ProtocolDevice(models.Model):
    protocol = models.ForeignKey(Protocol, related_name='protocol_pd', on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    firmware = models.ForeignKey(Firmware, on_delete=models.CASCADE, blank=True, null=True)
    sample = models.ForeignKey(DeviceSample, on_delete=models.CASCADE, blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='protocol_d_c', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, related_name='protocol_d_u', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(default=timezone.now)


class ProtocolScan(models.Model):
    protocol = models.ForeignKey(Protocol, on_delete=models.CASCADE)
    scan = models.FileField(upload_to="protocol/files/")
    created_by = models.ForeignKey(User, related_name='protocol_scan_c', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, related_name='protocol_scan_u', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(default=timezone.now)


class ProtocolTestResult(models.Model):
    protocol = models.ForeignKey(Protocol, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    result = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, related_name='protocol_test_result_c', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, related_name='protocol_test_result_u', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(default=timezone.now)
