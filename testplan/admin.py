from django.contrib import admin
from testplan.models import Testplan, Category, Chapter, Test, TestConfig


admin.site.register(Testplan)
admin.site.register(Category)
admin.site.register(Chapter)
admin.site.register(Test)
admin.site.register(TestConfig)
