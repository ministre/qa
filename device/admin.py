from django.contrib import admin
from device.models import CustomField, CustomFieldItem, CustomValue, DeviceType, Vendor, Device, DevicePhoto

admin.site.register(CustomField)
admin.site.register(CustomFieldItem)
admin.site.register(CustomValue)
admin.site.register(DeviceType)
admin.site.register(Vendor)
admin.site.register(Device)
admin.site.register(DevicePhoto)
