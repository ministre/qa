from django.contrib import admin
from testplan.models import TestplanPattern, TestplanPatternCategory, TestplanChecklist, Testplan, TestplanChapter


admin.site.register(TestplanPattern)
admin.site.register(TestplanPatternCategory)
admin.site.register(Testplan)
admin.site.register(TestplanChapter)
admin.site.register(TestplanChecklist)

