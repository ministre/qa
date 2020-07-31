from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Pattern(models.Model):
    name = models.CharField(max_length=1000)
    redmine_parent = models.CharField(max_length=1000, blank=True, null=True, default='patterns')
    redmine_project = models.CharField(max_length=1000, blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='pattern_c', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)
    updated_by = models.ForeignKey(User, related_name='pattern_u', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name

    def update_timestamp(self, user):
        self.updated_by = user
        self.updated_at = datetime.now()
        self.save()
        return True


class PatternCategory(models.Model):
    name = models.CharField(max_length=1000)
    pattern = models.ForeignKey(Pattern, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
