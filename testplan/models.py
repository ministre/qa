from django.db import models
from device.models import DeviceType


class TestplanPattern(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class TestplanPatternCategory(models.Model):
    name = models.CharField(max_length=1000)
    pattern = models.ForeignKey(TestplanPattern, on_delete=models.CASCADE)
    queue = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Testplan Pattern Categories"
        ordering = ('queue',)


class TestplanChecklist(models.Model):
    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Testplan Checklists"


class Testplan(models.Model):
    name = models.CharField(max_length=1000)
    version = models.CharField(max_length=300)
    device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class TestplanChapter(models.Model):
    testplan = models.ForeignKey(Testplan, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    text = models.TextField(max_length=100000)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Testplan Chapters"


class TestplanCategory(models.Model):
    name = models.CharField(max_length=1000)
    testplan = models.ForeignKey(Testplan, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Testplan Categories"
