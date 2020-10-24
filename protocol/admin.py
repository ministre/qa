from django.contrib import admin
from .models import Branch, Protocol, ProtocolDevice, ProtocolScan, ProtocolTestResult, TestResultIssue, \
    TestResultComment, TestResultImage, TestResultFile

admin.site.register(Branch)
admin.site.register(Protocol)
admin.site.register(ProtocolDevice)
admin.site.register(ProtocolScan)
admin.site.register(ProtocolTestResult)
admin.site.register(TestResultIssue)
admin.site.register(TestResultComment)
admin.site.register(TestResultImage)
admin.site.register(TestResultFile)
