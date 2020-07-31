from django.urls import path
from . import views

urlpatterns = [
    path('', views.PatternListView.as_view(), name='patterns'),
    path('create/', views.PatternCreate.as_view(), name='pattern_create'),
    path('update/<int:pk>/', views.PatternUpdate.as_view(), name='pattern_update'),
    path('delete/<int:pk>/', views.PatternDelete.as_view(), name='pattern_delete'),
    path('<int:pk>/<int:tab_id>/', views.pattern_details, name='pattern_details'),
]
