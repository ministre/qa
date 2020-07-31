from django.urls import path
from . import views

urlpatterns = [
    path('', views.PatternListView.as_view(), name='patterns'),
    path('create/', views.PatternCreate.as_view(), name='pattern_create'),
    path('<int:pk>/<int:tab_id>/', views.pattern_details, name='pattern_details'),
]
