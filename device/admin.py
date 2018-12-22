from django.contrib import admin
from device.models import CustomField, DeviceType, Device, DevicePhoto

# Register your models here.
admin.site.register(CustomField)
admin.site.register(DeviceType)
admin.site.register(Device)
admin.site.register(DevicePhoto)
