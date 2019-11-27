from django.contrib import admin
from device.models import CustomField, CustomValue, DeviceType, Vendor, Device, DevicePhoto

admin.site.register(CustomField)
admin.site.register(CustomValue)
admin.site.register(DeviceType)
admin.site.register(Vendor)
admin.site.register(Device)
admin.site.register(DevicePhoto)
