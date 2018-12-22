from django.contrib import admin
from device.models import DeviceType, CustomField

# Register your models here.
admin.site.register(DeviceType)
admin.site.register(CustomField)
