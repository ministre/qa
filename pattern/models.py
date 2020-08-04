from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Pattern(models.Model):
    name = models.CharField(max_length=1000)
    redmine_parent = models.CharField(max_length=1000, blank=True, null=True, default='patterns')
    redmine_project = models.CharField(max_length=1000, blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='p_c', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)
    updated_by = models.ForeignKey(User, related_name='p_u', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name


class PatternCategory(models.Model):
    pattern = models.ForeignKey(Pattern, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    priority = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, related_name='p_c_c', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)
    updated_by = models.ForeignKey(User, related_name='p_c_u', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Pattern Categories"
