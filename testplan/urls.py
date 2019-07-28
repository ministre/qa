from django.urls import path
from . import views

urlpatterns = [
    path('pattern/', views.TestplanPatternListView.as_view(), name='testplan_pattern_list'),
    path('pattern/create/', views.TestplanPatternCreate.as_view(), name='testplan_pattern_create'),
    path('pattern/<int:pk>/', views.testplan_pattern_details, name='testplan_pattern_details'),
    path('pattern/update/<int:pk>/', views.TestplanPatternUpdate.as_view(), name='testplan_pattern_update'),
    path('pattern/delete/<int:pk>/', views.TestplanPatternDelete.as_view(), name='testplan_pattern_delete'),
    path('pattern/<int:pk>/category/create/', views.testplan_pattern_category_create,
         name='testplan_pattern_category_create'),
    path('pattern/category/<int:pk>/', views.TestplanPatternCategoryUpdate.as_view(),
         name='testplan_pattern_category_update'),
    path('checklist/', views.TestplanChecklistListView.as_view(), name='testplan_checklist_list'),
]
