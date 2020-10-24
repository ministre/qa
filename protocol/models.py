from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from testplan.models import Testplan, Test
from device.models import Device, Firmware, DeviceSample
from django.core.validators import MinValueValidator
import os


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
    result = models.IntegerField(default=1)
    created_by = models.ForeignKey(User, related_name='protocol_test_result_c', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, related_name='protocol_test_result_u', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(default=timezone.now)


class TestResultIssue(models.Model):
    result = models.ForeignKey(ProtocolTestResult, related_name='result_issue', on_delete=models.CASCADE)
    text = models.TextField(max_length=100000)
    ticket = models.CharField(max_length=1000, blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='tr_issue_c', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, related_name='tr_issue_u', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text


class TestResultComment(models.Model):
    result = models.ForeignKey(ProtocolTestResult, related_name='result_comment', on_delete=models.CASCADE)
    text = models.TextField(max_length=100000)
    created_by = models.ForeignKey(User, related_name='tr_comment_c', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, related_name='tr_comment_u', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text


class TestResultImage(models.Model):
    result = models.ForeignKey(ProtocolTestResult, related_name='result_image', on_delete=models.CASCADE)
    desc = models.CharField(max_length=1000, blank=True, null=True)
    image = models.ImageField(upload_to="protocol/test_results/images/")
    width = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    height = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='tr_image_c', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, related_name='tr_image_u', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(default=timezone.now)


class TestResultFile(models.Model):
    result = models.ForeignKey(ProtocolTestResult, related_name='result_file', on_delete=models.CASCADE)
    desc = models.CharField(max_length=1000, blank=True, null=True)
    file = models.FileField(upload_to="protocol/test_results/files/")
    created_by = models.ForeignKey(User, related_name='tr_file_c', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, related_name='tr_file_u', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(default=timezone.now)

    def filename(self):
        return os.path.basename(self.file.name)
