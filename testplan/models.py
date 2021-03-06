from django.db import models
from device.models import DeviceType
from django.contrib.auth.models import User
from django.utils import timezone


class Testplan(models.Model):
    name = models.CharField(max_length=1000)
    version = models.CharField(max_length=300)
    device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(User, related_name='testplan_c', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, related_name='testplan_u', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)
    redmine_parent = models.CharField(max_length=1000, blank=True, null=True)
    redmine_project = models.CharField(max_length=1000, blank=True, null=True)
    members = models.ManyToManyField(User, related_name='members', blank=True)

    def __str__(self):
        return str(self.name) + ' (' + str(self.version) + ')'

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
    text = models.TextField(max_length=100000, blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='chapter_c', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, related_name='chapter_u', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)
    redmine_wiki = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.name

    def update_details(self, name: str, text: str, user):
        self.name = name
        self.text = text
        self.updated_at = timezone.now
        self.updated_by = user
        self.save()
        return [True, 'Data updated']


class Category(models.Model):
    testplan = models.ForeignKey(Testplan, related_name='testplan_category', on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    priority = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, related_name='t_c_c', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, related_name='t_c_u', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Testplan Categories"


class Test(models.Model):
    category = models.ForeignKey(Category, related_name='category_test', on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    purpose = models.TextField(max_length=5000, null=True, blank=True)
    procedure = models.TextField(null=True, blank=True)
    expected = models.TextField(null=True, blank=True)
    priority = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, related_name='t_t_c', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(User, related_name='t_t_u', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)
    redmine_wiki = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.name

    def update_details(self, name: str, purpose: str, procedure: str, expected: str, clear_configs: bool, configs: list,
                       images: list, files: list, clear_checklists: bool, checklists: list, clear_links: bool,
                       links: list, clear_comments: bool, comments: list):
        if name:
            self.name = name
        if purpose:
            self.purpose = purpose
        if procedure:
            self.procedure = procedure
        if expected:
            self.expected = expected

        if clear_configs:
            TestConfig.objects.filter(test=self).delete()

        if configs:
            for config in configs:
                TestConfig.objects.create(test=self, name=config[0], lang=config[1], config=config[2])

        if clear_checklists:
            TestChecklist.objects.filter(test=self).delete()

        if checklists:
            for checklist in checklists:
                new_checklist = TestChecklist.objects.create(test=self, name=checklist['name'])
                for item in checklist['items']:
                    TestChecklistItem.objects.create(checklist=new_checklist, name=item)

        if clear_links:
            TestLink.objects.filter(test=self).delete()

        if links:
            for link in links:
                TestLink.objects.create(test=self, name=link[0], url=link[1])

        if clear_comments:
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

    def __str__(self):
        return self.name


class TestChecklist(models.Model):
    test = models.ForeignKey(Test, related_name='test_checklist', on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class TestChecklistItem(models.Model):
    checklist = models.ForeignKey(TestChecklist, related_name='test_checklist_item', on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class TestIntegerValue(models.Model):
    test = models.ForeignKey(Test, related_name='test_integer_value', on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    unit = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class TestLink(models.Model):
    name = models.CharField(max_length=1000)
    url = models.CharField(max_length=1000)
    test = models.ForeignKey(Test, related_name='test_link', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class TestComment(models.Model):
    name = models.CharField(max_length=1000, blank=True, null=True)
    text = models.TextField(max_length=100000)
    test = models.ForeignKey(Test, related_name='test_comment', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
