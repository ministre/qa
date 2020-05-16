from django.contrib import admin
from .models import Testplan, Category, Chapter, Test, TestConfig, TestImage, TestFile,\
    TestWorksheet, TestWorksheetItem, TestChecklist, TestChecklistItem, TestLink, TestComment, Pattern

admin.site.register(Testplan)
admin.site.register(Category)
admin.site.register(Chapter)
admin.site.register(Test)
admin.site.register(TestConfig)
admin.site.register(TestImage)
admin.site.register(TestFile)
admin.site.register(TestWorksheet)
admin.site.register(TestWorksheetItem)
admin.site.register(TestChecklist)
admin.site.register(TestChecklistItem)
admin.site.register(TestLink)
admin.site.register(TestComment)
admin.site.register(Pattern)
