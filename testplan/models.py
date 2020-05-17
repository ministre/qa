from django.db import models
from device.models import DeviceType
from django.contrib.auth.models import User
from datetime import datetime


class Testplan(models.Model):
    name = models.CharField(max_length=1000)
    version = models.CharField(max_length=300)
    device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(User, related_name='testplan_c', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='testplan_u', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)
    redmine_parent = models.CharField(max_length=1000, blank=True, null=True)
    redmine_project = models.CharField(max_length=1000, blank=True, null=True)
    members = models.ManyToManyField(User, related_name='members', blank=True)

    def __str__(self):
        return self.name

    def update_timestamp(self, user):
        self.updated_by = user
        self.updated_at = datetime.now()
        self.save()
        return True

    def tests_count(self):
        count = 0
        for category in Category.objects.filter(testplan=self):
            tests = Test.objects.filter(category=category)
            count += tests.count()
        return count

    def protocols_count(self):
        from protocol.models import Protocol
        count = Protocol.objects.filter(testplan=self).count()
        return count


class Chapter(models.Model):
    testplan = models.ForeignKey(Testplan, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    text = models.TextField(max_length=100000)
    created_by = models.ForeignKey(User, related_name='chapter_c', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='chapter_u', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)
    redmine_url = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=1000)
    testplan = models.ForeignKey(Testplan, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Test(models.Model):
    category = models.ForeignKey(Category, related_name='category_test', on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    purpose = models.TextField(max_length=5000, null=True, blank=True)
    procedure = models.TextField(null=True, blank=True)
    expected = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='test_c', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='test_u', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)
    redmine_wiki = models.CharField(max_length=1000, null=True, blank=True)

    def update_timestamp(self, user):
        self.updated_by = user
        self.updated_at = datetime.now()
        self.save()
        return True

    def update_details(self, name, purpose, procedure, expected, configs, images, files, checklists,
                       links, comments):
        if name:
            self.name = name
        if purpose:
            self.purpose = purpose
        if procedure:
            self.procedure = procedure
        if expected:
            self.expected = expected

        TestConfig.objects.filter(test=self).delete()
        if configs:
            for config in configs:
                TestConfig.objects.create(test=self, name=config[0], lang=config[1], config=config[2])

        TestChecklist.objects.filter(test=self).delete()
        if checklists:
            for checklist in checklists:
                new_checklist = TestChecklist.objects.create(test=self, name=checklist['name'])
                for item in checklist['items']:
                    TestChecklistItem.objects.create(checklist=new_checklist, name=item)

        TestLink.objects.filter(test=self).delete()
        if links:
            for link in links:
                TestLink.objects.create(test=self, name=link[0], url=link[1])

        TestComment.objects.filter(test=self).delete()
        if comments:
            for comment in comments:
                TestComment.objects.create(test=self, name=comment[0], text=comment[1])
        self.save()
        return True


class TestConfig(models.Model):
    name = models.CharField(max_length=1000, blank=True, null=True)
    lang = models.CharField(max_length=40, blank=True, null=True)
    test = models.ForeignKey(Test, related_name='test_config', on_delete=models.CASCADE)
    config = models.TextField(null=True, blank=True)


class TestImage(models.Model):
    name = models.CharField(max_length=1000, blank=True, null=True)
    test = models.ForeignKey(Test, related_name='test_image', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="testplan/images/")
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)


class TestFile(models.Model):
    name = models.CharField(max_length=1000, blank=True, null=True)
    test = models.ForeignKey(Test, related_name='test_file', on_delete=models.CASCADE)
    file = models.FileField(upload_to="testplan/files/")


class TestWorksheet(models.Model):
    name = models.CharField(max_length=1000)
    test = models.ForeignKey(Test, related_name='test_worksheet', on_delete=models.CASCADE)
    type = models.CharField(max_length=10, default='Text')


class TestWorksheetItem(models.Model):
    name = models.CharField(max_length=1000)
    worksheet = models.ForeignKey(TestWorksheet, related_name='worksheet_item', on_delete=models.CASCADE)


class TestChecklist(models.Model):
    test = models.ForeignKey(Test, related_name='test_checklist', on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)


class TestChecklistItem(models.Model):
    checklist = models.ForeignKey(TestChecklist, related_name='test_checklist_item', on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)


class TestLink(models.Model):
    name = models.CharField(max_length=1000)
    url = models.CharField(max_length=1000)
    test = models.ForeignKey(Test, related_name='test_link', on_delete=models.CASCADE)


class TestComment(models.Model):
    name = models.CharField(max_length=1000, blank=True, null=True)
    text = models.TextField(max_length=100000)
    test = models.ForeignKey(Test, related_name='test_comment', on_delete=models.CASCADE)


class Pattern(models.Model):
    name = models.CharField(max_length=1000)
    types = models.ManyToManyField(DeviceType, related_name='device_types', blank=True)
    redmine_parent = models.CharField(max_length=1000, blank=True, null=True)
    redmine_project = models.CharField(max_length=1000, blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='pattern_c', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='pattern_u', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.name

    def update_timestamp(self, user):
        self.updated_by = user
        self.updated_at = datetime.now()
        self.save()
        return True


class PatternTitle(models.Model):
    pattern = models.ForeignKey(Pattern, on_delete=models.CASCADE)
    device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)

    class Meta:
        unique_together = ('pattern', 'device_type',)
