from django.contrib import admin
from testplan.models import TestplanChecklist, Testplan, TestplanCategory, TestplanChapter, Test


admin.site.register(Testplan)
admin.site.register(TestplanCategory)
admin.site.register(TestplanChapter)
admin.site.register(TestplanChecklist)
admin.site.register(Test)
