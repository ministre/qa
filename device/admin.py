from django.contrib import admin
from device.models import CustomField, CustomValue, DeviceType, Vendor, Device, DevicePhoto, Interface, DeviceInterface

admin.site.register(CustomField)
admin.site.register(CustomValue)
admin.site.register(Interface)
admin.site.register(DeviceType)
admin.site.register(Vendor)
admin.site.register(Device)
admin.site.register(DevicePhoto)
admin.site.register(DeviceInterface)
