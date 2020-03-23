from django.contrib import admin
from .models import Resolution, Protocol, TestResult

admin.site.register(Resolution)
admin.site.register(Protocol)
admin.site.register(TestResult)
