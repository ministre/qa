from django.db import models


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
