from django.contrib import admin
from .models import Branch, Protocol, ProtocolDevice, ProtocolScan, ProtocolTestResult

admin.site.register(Branch)
admin.site.register(Protocol)
admin.site.register(ProtocolDevice)
admin.site.register(ProtocolScan)
admin.site.register(ProtocolTestResult)
