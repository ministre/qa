from django.contrib import admin
from .models import Branch, Protocol, ProtocolDevice, ProtocolScan

admin.site.register(Branch)
admin.site.register(Protocol)
admin.site.register(ProtocolDevice)
admin.site.register(ProtocolScan)
