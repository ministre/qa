from django.contrib import admin
from device.models import Vendor, DeviceChecklist, DeviceChecklistItem, DeviceSlist, DeviceSlistItem, \
    DeviceTextField, DeviceIntegerField, DeviceType, DeviceTypeSpecification, CustomField, CustomFieldItem, \
    CustomValue, Device, DevicePhoto, Sample

admin.site.register(Vendor)
admin.site.register(DeviceChecklist)
admin.site.register(DeviceChecklistItem)
admin.site.register(DeviceSlist)
admin.site.register(DeviceSlistItem)
admin.site.register(DeviceTextField)
admin.site.register(DeviceIntegerField)
admin.site.register(DeviceType)
admin.site.register(DeviceTypeSpecification)
admin.site.register(CustomField)
admin.site.register(CustomFieldItem)
admin.site.register(CustomValue)
admin.site.register(Device)
admin.site.register(DevicePhoto)
admin.site.register(Sample)
