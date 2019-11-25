from django.db import models
from device.models import DeviceType
from django.contrib.auth.models import User
from datetime import datetime


class Testplan(models.Model):
    name = models.CharField(max_length=1000)
    version = models.CharField(max_length=300)
    device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(User, related_name='testplan_created_by_user', on_delete=models.CASCADE,
                                   blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='testplan_updated_by_user', on_delete=models.CASCADE,
                                   blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)
    redmine_url = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.name


class Chapter(models.Model):
    testplan = models.ForeignKey(Testplan, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    text = models.TextField(max_length=100000)
    created_by = models.ForeignKey(User, related_name='chapter_created_by_user', on_delete=models.CASCADE,
                                   blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='chapter_updated_by_user', on_delete=models.CASCADE,
                                   blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)
    redmine_url = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Chapters"


class Category(models.Model):
    name = models.CharField(max_length=1000)
    testplan = models.ForeignKey(Testplan, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Test(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    purpose = models.TextField(max_length=5000, null=True, blank=True)
    procedure = models.TextField(null=True, blank=True)
    expected = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='test_created_by_user', on_delete=models.CASCADE,
                                   blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='test_updated_by_user', on_delete=models.CASCADE,
                                   blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)
    redmine_url = models.CharField(max_length=1000, null=True, blank=True)


class TestConfig(models.Model):
    name = models.CharField(max_length=1000, blank=True, null=True)
    lang = models.CharField(max_length=40, blank=True, null=True)
    test = models.ForeignKey(Test, related_name='test_config', on_delete=models.CASCADE)
    config = models.TextField(null=True, blank=True)


class TestImage(models.Model):
    name = models.CharField(max_length=1000, blank=True, null=True)
    test = models.ForeignKey(Test, related_name='test_image', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="testplan/images/")


class TestFile(models.Model):
    name = models.CharField(max_length=1000, blank=True, null=True)
    test = models.ForeignKey(Test, related_name='test_file', on_delete=models.CASCADE)
    file = models.FileField(upload_to="testplan/files/")


class TestChecklist(models.Model):
    name = models.CharField(max_length=1000)
    test = models.ForeignKey(Test, related_name='test_checklist', on_delete=models.CASCADE)


class ChecklistItem(models.Model):
    name = models.CharField(max_length=1000)
    checklist = models.ForeignKey(TestChecklist, related_name='checklist_item', on_delete=models.CASCADE)


class TestWorksheet(models.Model):
    name = models.CharField(max_length=1000)
    test = models.ForeignKey(Test, related_name='test_worksheet', on_delete=models.CASCADE)


class WorksheetItem(models.Model):
    name = models.CharField(max_length=1000)
    worksheet = models.ForeignKey(TestWorksheet, related_name='worksheet_item', on_delete=models.CASCADE)


class TestLink(models.Model):
    name = models.CharField(max_length=1000)
    url = models.CharField(max_length=1000)
    test = models.ForeignKey(Test, related_name='test_link', on_delete=models.CASCADE)


class TestComment(models.Model):
    text = models.TextField(max_length=100000)
    test = models.ForeignKey(Test, related_name='test_comment', on_delete=models.CASCADE)


class Pattern(models.Model):
    name = models.CharField(max_length=1000)
    types = models.ManyToManyField(DeviceType, related_name='device_types', blank=True)
    created_by = models.ForeignKey(User, related_name='pattern_created_by_user', on_delete=models.CASCADE,
                                   blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='pattern_updated_by_user', on_delete=models.CASCADE,
                                   blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)
    redmine_url = models.CharField(max_length=1000, blank=True, null=True)
