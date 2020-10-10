from django.contrib import admin
from .models import Branch, Resolution, Protocol, TestResult

admin.site.register(Branch)
admin.site.register(Resolution)
admin.site.register(Protocol)
admin.site.register(TestResult)
