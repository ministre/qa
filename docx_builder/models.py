from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class DocxProfile(models.Model):
    name = models.CharField(max_length=1000)
    created_by = models.ForeignKey(User, related_name='docx_profile_c', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='docx_profile_u', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.name

    def update_timestamp(self, user):
        self.updated_by = user
        self.updated_at = datetime.now()
        self.save()
        return True
