from django.contrib import admin
from .models import Branch, Protocol, ProtocolDevice, ProtocolScan, ProtocolTestResult, TestResultConfig, \
    TestResultImage, TestResultFile, TestResultIssue, TestResultComment

admin.site.register(Branch)
admin.site.register(Protocol)
admin.site.register(ProtocolDevice)
admin.site.register(ProtocolScan)
admin.site.register(ProtocolTestResult)
admin.site.register(TestResultConfig)
admin.site.register(TestResultImage)
admin.site.register(TestResultFile)
admin.site.register(TestResultIssue)
admin.site.register(TestResultComment)
