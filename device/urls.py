from django.urls import path
from . import views

urlpatterns = [
    path('', views.device_list, name='device_list'),
    path('type/', views.device_type_list, name='device_type_list'),
    path('type/add/', views.device_type_add, name='device_type_add'),
    path('type/<int:pk>/', views.device_type_edit, name='device_type_edit'),
    path('type/<int:pk>/delete/', views.device_type_delete, name='device_type_delete'),
]
