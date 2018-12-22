from django.db import models


class CustomField(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class DeviceType(models.Model):
    tag = models.CharField(max_length=100)
    desc = models.CharField(max_length=300)
    cf = models.ManyToManyField(CustomField)
