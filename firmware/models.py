#from django.db import models
#from device.models import Device
#from django.contrib.auth.models import User
#from datetime import datetime


#class Firmware(models.Model):
#    device = models.ForeignKey(Device, on_delete=models.CASCADE)
#    version = models.CharField(max_length=300)
#    desc = models.CharField(max_length=1000, blank=True, null=True)
#    file = models.FileField(upload_to="firmware/files/", blank=True, null=True)
#    checksum = models.CharField(max_length=300, blank=True, null=True)
#    sysinfo_cli = models.TextField(null=True, blank=True)
#    sysinfo_snapshot = models.ImageField(upload_to="firmware/snapshots/", null=True, blank=True)
#    created_by = models.ForeignKey(User, related_name='firmware_created_by', on_delete=models.CASCADE,
#                                   blank=True, null=True)
#    created_at = models.DateTimeField(default=datetime.now, blank=True)
#    updated_by = models.ForeignKey(User, related_name='firmware_updated_by', on_delete=models.CASCADE,
#                                   blank=True, null=True)
#    updated_at = models.DateTimeField(default=datetime.now, blank=True)
#
#    def __str__(self):
#        return self.version
