from django.urls import path
from . import views

urlpatterns = [
    path('', views.PatternListView.as_view(), name='patterns'),
    path('create/', views.PatternCreate.as_view(), name='pattern_create'),
    path('<int:pk>/', views.PatternUpdate.as_view(), name='pattern_update'),
    path('<int:pk>/delete/', views.PatternDelete.as_view(), name='pattern_delete'),
]
