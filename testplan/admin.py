from django.contrib import admin
from testplan.models import TestplanPattern, TestplanPatternCategory, TestplanChecklist, \
    Testplan, TestplanCategory, TestplanChapter


admin.site.register(Testplan)
admin.site.register(TestplanCategory)
admin.site.register(TestplanChapter)
admin.site.register(TestplanChecklist)
admin.site.register(TestplanPattern)
admin.site.register(TestplanPatternCategory)
