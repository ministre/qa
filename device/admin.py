from django.contrib import admin
from device.models import Vendor, DeviceChecklist, DeviceChecklistItem, DeviceChecklistItemValue, DeviceSlist, \
    DeviceSlistItem, DeviceSlistItemValue, DeviceTextField, DeviceTextFieldValue, DeviceIntegerField, \
    DeviceIntegerFieldValue, DeviceType, DeviceTypeSpecification, Device, DevicePhoto, Sample, Firmware, FirmwareAccount

admin.site.register(Vendor)
admin.site.register(DeviceChecklist)
admin.site.register(DeviceChecklistItem)
admin.site.register(DeviceChecklistItemValue)
admin.site.register(DeviceSlist)
admin.site.register(DeviceSlistItem)
admin.site.register(DeviceSlistItemValue)
admin.site.register(DeviceTextField)
admin.site.register(DeviceTextFieldValue)
admin.site.register(DeviceIntegerField)
admin.site.register(DeviceIntegerFieldValue)
admin.site.register(DeviceType)
admin.site.register(DeviceTypeSpecification)
admin.site.register(Device)
admin.site.register(DevicePhoto)
admin.site.register(Sample)
admin.site.register(Firmware)
admin.site.register(FirmwareAccount)
