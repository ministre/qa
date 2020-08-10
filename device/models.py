from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist


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

    def update_timestamp(self, user):
        self.updated_by = user
        self.updated_at = datetime.now()
        self.save()
        return True


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

    def update_timestamp(self, user):
        self.updated_by = user
        self.updated_at = datetime.now()
        self.save()
        return True


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

    def update_timestamp(self, user):
        self.updated_by = user
        self.updated_at = datetime.now()
        self.save()
        return True


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

    def update_timestamp(self, user):
        self.updated_by = user
        self.updated_at = datetime.now()
        self.save()
        return True


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

    def update_timestamp(self, user):
        self.updated_by = user
        self.updated_at = datetime.now()
        self.save()
        return True


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
    # cf = models.ManyToManyField(CustomField, related_name='custom_fields', blank=True)
    redmine_parent = models.CharField(max_length=1000, blank=True, null=True)
    redmine_project = models.CharField(max_length=1000, blank=True, null=True)
    redmine_project_name = models.CharField(max_length=1000, blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='type_c', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='type_u', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.desc

    def update_timestamp(self, user):
        self.updated_by = user
        self.updated_at = datetime.now()
        self.save()
        return True

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
    hw = models.CharField(max_length=100)
    redmine_project = models.CharField(max_length=1000, blank=True, null=True)
    # members = models.ManyToManyField(User, related_name='device_members', blank=True)
    created_by = models.ForeignKey(User, related_name='device_c', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='device_u', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.model

    def update_timestamp(self, user):
        self.updated_by = user
        self.updated_at = datetime.now()
        self.save()
        return True


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


class Specification:
    def __init__(self):
        self.specs = []  # [{'name': <>, 'values': [<>, ]}]
        self.form_metadata = []
        # [{'name': <>, 'type': <>, 'id': <>, 'value': <>, 'items': [{'name': <>, 'id': <>, 'selected': <bool>}, ]}]

    def get_values(self, device: Device):
        for field in CustomField.objects.filter(custom_fields__id=device.type.id).order_by('id'):
            values = []
            for value in CustomValue.objects.filter(Q(field=field) & Q(device=device)):
                if value.item:
                    values.append(value.item)
                else:
                    values.append(value.value)
            self.specs.append({'name': field.name, 'values': values})
        return self.specs

    def get_form_metadata(self, device: Device):
        for field in CustomField.objects.filter(custom_fields__id=device.type.id).order_by('id'):
            items = []
            if field.type == 'text' or field.type == 'number':
                try:
                    value = CustomValue.objects.get(Q(field=field) & Q(device=device))
                    self.form_metadata.append({'name': field.name, 'type': field.type, 'id': field.id,
                                               'value': value.value, 'items': items})
                except ObjectDoesNotExist:
                    self.form_metadata.append({'name': field.name, 'type': field.type, 'id': field.id,
                                               'value': '', 'items': items})
            if field.type == 'listbox' or field.type == 'checkbox':
                for item in CustomFieldItem.objects.filter(custom_field=field):
                    try:
                        CustomValue.objects.get(Q(item=item) & Q(device=device))
                        items.append({'name': item.name, 'id': item.id, 'selected': True})
                    except ObjectDoesNotExist:
                        items.append({'name': item.name, 'id': item.id, 'selected': False})
                self.form_metadata.append({'name': field.name, 'type': field.type, 'id': field.id, 'value': None,
                                           'items': items})
        return self.form_metadata

    def update_value(self, device: Device, field_id: int, value: str):
        field = CustomField.objects.get(id=field_id)
        if field.type == 'text' or field.type == 'number':
            if value:
                CustomValue.objects.update_or_create(device=device, field=field, defaults={"value": value})
            else:
                CustomValue.objects.filter(Q(device=device) & Q(field=field)).delete()
            return True
        elif field.type == 'listbox':
            if value:
                CustomValue.objects.update_or_create(device=device, field=field,
                                                     defaults={"item": CustomFieldItem.objects.get(id=value)})
            else:
                CustomValue.objects.filter(Q(device=device) & Q(field=field)).delete()
        elif field.type == 'checkbox':
            pass
        return True

    def update_checkbox(self, device: Device, field_id: int, item_id: int):
        if item_id == 0:
            CustomValue.objects.filter(Q(device=device) & Q(field=CustomField.objects.get(id=field_id))).delete()
        else:
            CustomValue.objects.create(device=device, field=CustomField.objects.get(id=field_id),
                                       item=CustomFieldItem.objects.get(id=item_id))
        return True


class Firmware(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    version = models.CharField(max_length=300)
    description = models.CharField(max_length=1000, blank=True, null=True)
    changelog = models.TextField(null=True, blank=True)
    checksum = models.CharField(max_length=300, blank=True, null=True)
    # file = models.FileField(upload_to="device/firmware/", blank=True, null=True)
    # sysinfo_cli = models.TextField(null=True, blank=True)
    # sysinfo_snapshot = models.ImageField(upload_to="firmware/snapshots/", null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='firmware_c', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='firmware_u', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.version
