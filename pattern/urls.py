from django.urls import path
from . import views

urlpatterns = [
    path('', views.PatternListView.as_view(), name='patterns'),
]
