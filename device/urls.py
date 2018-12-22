from django.urls import path
from . import views

urlpatterns = [
    path('', views.DeviceListView.as_view(), name='device_list'),
    path('type/', views.DeviceTypeListView.as_view(), name='type_list'),
    path('type/create/', views.DeviceTypeCreate.as_view(), name='type_create'),
    path('type/<int:pk>/', views.DeviceTypeUpdate.as_view(), name='type_update'),
    path('type/<int:pk>/delete/', views.DeviceTypeDelete.as_view(), name='type_delete'),
    path('custom_field/', views.CustomFieldListView.as_view(), name='custom_field_list'),
    path('custom_field/create/', views.CustomFieldCreate.as_view(), name='custom_field_create'),
    path('custom_field/<int:pk>/', views.CustomFieldUpdate.as_view(), name='custom_field_update'),
    path('custom_field/<int:pk>/delete/', views.CustomFieldDelete.as_view(), name='custom_field_delete'),
    path('device/create/', views.DeviceCreate.as_view(), name='device_create'),
    path('device/<int:pk>/', views.DeviceUpdate.as_view(), name='device_update'),
    path('device/<int:pk>/delete/', views.DeviceDelete.as_view(), name='device_delete'),
    path('photo/', views.DevicePhotoListView.as_view(), name='photo_list'),
    path('photo/create/', views.DevicePhotoCreate.as_view(), name='photo_create'),
    path('photo/<int:pk>/', views.DevicePhotoUpdate.as_view(), name='photo_update'),
    path('photo/<int:pk>/delete/', views.DevicePhotoDelete.as_view(), name='photo_delete'),
]
