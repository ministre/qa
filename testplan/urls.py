from django.urls import path
from . import views

urlpatterns = [
    path('pattern/', views.TestplanPatternListView.as_view(), name='testplan_pattern_list'),
]
