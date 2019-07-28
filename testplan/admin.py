from django.contrib import admin
from testplan.models import TestplanPattern, TestplanPatternCategory, TestplanChecklist


admin.site.register(TestplanPattern)
admin.site.register(TestplanPatternCategory)
admin.site.register(TestplanChecklist)
