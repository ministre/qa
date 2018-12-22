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
    cf = models.ManyToManyField(CustomField, blank=True, null=True)

    def __str__(self):
        return self.desc

    class Meta:
        ordering = ('desc',)


class Device(models.Model):
    vendor = models.CharField(max_length=300)
    model = models.CharField(max_length=300)
    hw = models.CharField(max_length=100)
    type = models.ForeignKey(DeviceType, on_delete=models.CASCADE)

    def __str__(self):
        return self.model
