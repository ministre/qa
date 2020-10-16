from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Vendor(models.Model):
    name = models.CharField(max_length=400)
    created_by = models.ForeignKey(User, related_name='vendor_c', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='vendor_u', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class DeviceChecklist(models.Model):
    name = models.CharField(max_length=500)
    desc = models.CharField(max_length=1000, blank=True, null=True)
    items_order_by = models.CharField(max_length=10, default='id')
    created_by = models.ForeignKey(User, related_name='d_checklist_c', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='d_checklist_u', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.name


class DeviceChecklistItem(models.Model):
    checklist = models.ForeignKey(DeviceChecklist, related_name='d_checklist_item', on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class DeviceSlist(models.Model):
    name = models.CharField(max_length=500)
    desc = models.CharField(max_length=1000, blank=True, null=True)
    items_order_by = models.CharField(max_length=10, default='id')
    created_by = models.ForeignKey(User, related_name='d_slist_c', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='d_slist_u', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.name


class DeviceSlistItem(models.Model):
    slist = models.ForeignKey(DeviceSlist, related_name='d_slist_item', on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class DeviceTextField(models.Model):
    name = models.CharField(max_length=500)
    desc = models.CharField(max_length=1000, blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='d_tfield_c', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='d_tfield_u', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.name


class DeviceIntegerField(models.Model):
    name = models.CharField(max_length=500)
    unit = models.CharField(max_length=100, blank=True, null=True)
    desc = models.CharField(max_length=1000, blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='d_ifield_c', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='d_ifield_u', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.name


class DeviceType(models.Model):
    tag = models.CharField(max_length=100)
    desc = models.CharField(max_length=1000)
    desc_genitive = models.CharField(max_length=1000, null=True, blank=True)
    redmine_parent = models.CharField(max_length=1000, blank=True, null=True)
    redmine_project = models.CharField(max_length=1000, blank=True, null=True)
    redmine_project_name = models.CharField(max_length=1000, blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='type_c', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='type_u', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.desc

    def devices_count(self):
        count = Device.objects.filter(type=self).count()
        return count

    def testplans_count(self):
        from testplan.models import Testplan
        count = Testplan.objects.filter(device_type=self).count()
        return count

    class Meta:
        ordering = ('desc',)


class DeviceTypeSpecification(models.Model):
    type = models.ForeignKey(DeviceType, on_delete=models.CASCADE)
    checklist = models.ForeignKey(DeviceChecklist, on_delete=models.CASCADE, blank=True, null=True)
    slist = models.ForeignKey(DeviceSlist, on_delete=models.CASCADE, blank=True, null=True)
    text_field = models.ForeignKey(DeviceTextField, on_delete=models.CASCADE, blank=True, null=True)
    integer_field = models.ForeignKey(DeviceIntegerField, on_delete=models.CASCADE, blank=True, null=True)

    def get_type(self):
        if self.checklist:
            return 'checklist'
        if self.slist:
            return 'slist'
        if self.text_field:
            return 'text_field'
        if self.integer_field:
            return 'integer_field'


class Device(models.Model):
    type = models.ForeignKey(DeviceType, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    model = models.CharField(max_length=400)
    hw = models.CharField(max_length=100, blank=True, null=True)
    redmine_project = models.CharField(max_length=1000, blank=True, null=True)
    # members = models.ManyToManyField(User, related_name='device_members', blank=True)
    created_by = models.ForeignKey(User, related_name='device_c', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='device_u', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.model


class DeviceChecklistItemValue(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    item = models.ForeignKey(DeviceChecklistItem, on_delete=models.CASCADE)
    value = models.BooleanField(blank=True, null=True)


class DeviceSlistItemValue(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    value = models.ForeignKey(DeviceSlistItem, on_delete=models.CASCADE, blank=True, null=True)


class DeviceTextFieldValue(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    field = models.ForeignKey(DeviceTextField, on_delete=models.CASCADE)
    value = models.CharField(max_length=2000, blank=True, null=True)


class DeviceIntegerFieldValue(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    field = models.ForeignKey(DeviceIntegerField, on_delete=models.CASCADE)
    value = models.IntegerField(blank=True, null=True)


class DevicePhoto(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="device/photos/")
    desc = models.CharField(max_length=500)
    created_by = models.ForeignKey(User, related_name='photo_c', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='photo_u', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)


class DeviceDocumentType(models.Model):
    name = models.CharField(max_length=300)
    created_by = models.ForeignKey(User, related_name='doc_type_c', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='doc_type_u', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.name


class DeviceDocument(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    type = models.ForeignKey(DeviceDocumentType, on_delete=models.CASCADE)
    file = models.FileField(upload_to="device/docs/")
    desc = models.CharField(max_length=300, blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='doc_c', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='doc_u', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)


class DeviceSample(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    sn = models.CharField(max_length=50, blank=True, null=True)
    desc = models.CharField(max_length=1000, blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='sample_c', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)
    updated_by = models.ForeignKey(User, related_name='sample_u', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        sample_name = '(ID: ' + str(self.id) + ')'
        if self.sn:
            sample_name += ' (SN: ' + str(self.sn) + ')'
        if self.desc:
            sample_name += ' (Description: ' + str(self.desc) + ')'
        return sample_name


class DeviceSampleAccount(models.Model):
    sample = models.ForeignKey(DeviceSample, related_name='sample_account', on_delete=models.CASCADE)
    username = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='sample_account_c', on_delete=models.CASCADE, blank=True,
                                   null=True)
    created_at = models.DateTimeField(default=datetime.now)
    updated_by = models.ForeignKey(User, related_name='sample_account_u', on_delete=models.CASCADE, blank=True,
                                   null=True)
    updated_at = models.DateTimeField(default=datetime.now)


class DeviceSupport(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    contact = models.ForeignKey('contact.Contact', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='d_support_c', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='d_support_u', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)


class Firmware(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    version = models.CharField(max_length=300)
    description = models.CharField(max_length=1000, blank=True, null=True)
    checksum = models.CharField(max_length=300, blank=True, null=True)
    changelog = models.TextField(null=True, blank=True)
    sysinfo = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='fw_c', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='fw_u', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.version


class FirmwareAccount(models.Model):
    firmware = models.ForeignKey(Firmware, on_delete=models.CASCADE)
    username = models.CharField(max_length=1000, blank=True, null=True)
    password = models.CharField(max_length=1000, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)


class FirmwareFile(models.Model):
    firmware = models.ForeignKey(Firmware, on_delete=models.CASCADE)
    file = models.FileField(upload_to="device/firmware/", blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)


class FirmwareScreenshot(models.Model):
    firmware = models.ForeignKey(Firmware, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="device/fw_screenshot")
    description = models.CharField(max_length=1000, blank=True, null=True)


class FirmwareHowto(models.Model):
    firmware = models.ForeignKey(Firmware, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000, blank=True, null=True)
    text = models.TextField(null=True, blank=True)
