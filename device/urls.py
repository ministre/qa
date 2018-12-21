from django.urls import path
from . import views

urlpatterns = [
    path('', views.device_list, name='device_list'),
    path('type/', views.DeviceTypeListView.as_view(), name='device_type_list'),
    path('type/add/', views.DeviceTypeCreate.as_view(), name='device_type_create'),
    path('type/<int:pk>/', views.DeviceTypeUpdate.as_view(), name='device_type_update'),
    path('type/<int:pk>/delete/', views.DeviceTypeDelete.as_view(), name='device_type_delete'),
#    path('type/<int:pk>/delete/', views.device_type_delete, name='device_type_delete'),
]
