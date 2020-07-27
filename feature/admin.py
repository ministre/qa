from django.contrib import admin
from .models import FeatureList, FeatureListCategory, FeatureListItem, FeatureListLink

admin.site.register(FeatureList)
admin.site.register(FeatureListCategory)
admin.site.register(FeatureListItem)
admin.site.register(FeatureListLink)
