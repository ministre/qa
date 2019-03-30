from django.urls import path
from . import views

urlpatterns = [
    path('pattern/', views.TestplanPatternListView.as_view(), name='testplan_pattern_list'),
    path('pattern/create/', views.TestplanPatternCreate.as_view(), name='testplan_pattern_create'),
    path('pattern/<int:pk>/', views.TestplanPatternUpdate.as_view(), name='testplan_pattern_update'),
    path('pattern/<int:pk>/delete/', views.TestplanPatternDelete.as_view(), name='testplan_pattern_delete'),
]
