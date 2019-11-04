from django.contrib import admin
from testplan.models import Checklist, Testplan, Category, Chapter, Test


admin.site.register(Testplan)
admin.site.register(Category)
admin.site.register(Chapter)
admin.site.register(Checklist)
admin.site.register(Test)
