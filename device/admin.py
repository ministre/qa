from django.contrib import admin
from device.models import CustomField, CustomValue, DeviceType, Device, DevicePhoto, Button, Led, Firmware

# Register your models here.
admin.site.register(CustomField)
admin.site.register(CustomValue)
admin.site.register(DeviceType)
admin.site.register(Device)
admin.site.register(DevicePhoto)
admin.site.register(Button)
admin.site.register(Led)
admin.site.register(Firmware)
