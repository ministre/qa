from django.db import models
from device.models import DeviceType
from django.contrib.auth.models import User
from datetime import datetime


class FeatureList(models.Model):
    device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    version = models.CharField(max_length=300)
    created_by = models.ForeignKey(User, related_name='fl_c', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='fl_u', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)
    redmine_wiki = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.name

    def update_timestamp(self, user):
        self.updated_by = user
        self.updated_at = datetime.now()
        self.save()
        return True

    def clear(self, user):
        FeatureListCategory.objects.filter(feature_list=self).delete()
        self.update_timestamp(user=user)
        return [True, 'Data cleared']

    def update_data(self, name: str, user, categories=None):
        if categories is None:
            categories = []
        self.name = name
        for category in categories:
            cat, created = FeatureListCategory.objects.update_or_create(feature_list=self, name=category['name'],
                                                                        defaults={'feature_list': self,
                                                                                  'name': category['name'],
                                                                                  'created_by': user,
                                                                                  'updated_by': user,
                                                                                  'updated_at': datetime.now})
            for item in category['items']:
                FeatureListItem.objects.update_or_create(category=cat, name=item['name'],
                                                         defaults={'category': cat,
                                                                   'name': item['name'],
                                                                   'optional': item['optional'],
                                                                   'created_by': user,
                                                                   'updated_by': user,
                                                                   'updated_at': datetime.now})
        self.save()
        self.update_timestamp(user=user)
        return [True, 'Data updated']


class FeatureListCategory(models.Model):
    feature_list = models.ForeignKey(FeatureList, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=1000)
    created_by = models.ForeignKey(User, related_name='flc_c', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='flc_u', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Feature List Categories"


class FeatureListItem(models.Model):
    category = models.ForeignKey(FeatureListCategory, related_name='category_item', on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    optional = models.BooleanField(blank=True, null=True, default=False)
    created_by = models.ForeignKey(User, related_name='fli_c', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='fli_u', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)
