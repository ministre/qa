from django.contrib import admin
from .models import FeatureList, FeatureListCategory, FeatureListItem

admin.site.register(FeatureList)
admin.site.register(FeatureListCategory)
admin.site.register(FeatureListItem)
