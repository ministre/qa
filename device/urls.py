from django.urls import path
from . import views

urlpatterns = [
    path('', views.DeviceListView.as_view(), name='devices'),

    # device types
    path('type/', views.DeviceTypeListView.as_view(), name='device_types'),
    path('type/create/', views.DeviceTypeCreate.as_view(), name='device_type_create'),
    path('type/<int:pk>/', views.DeviceTypeUpdate.as_view(), name='device_type_update'),
    path('type/<int:pk>/delete/', views.DeviceTypeDelete.as_view(), name='device_type_delete'),

    # device vendors
    path('vendor/', views.VendorListView.as_view(), name='vendors'),
    path('vendor/create/', views.VendorCreate.as_view(), name='vendor_create'),
    path('vendor/<int:pk>/', views.VendorUpdate.as_view(), name='vendor_update'),
    path('vendor/<int:pk>/delete/', views.VendorDelete.as_view(), name='vendor_delete'),

    path('custom_field/', views.CustomFieldListView.as_view(), name='custom_field_list'),
    path('custom_field/create/', views.CustomFieldCreate.as_view(), name='custom_field_create'),
    path('custom_field/<int:pk>/', views.CustomFieldUpdate.as_view(), name='custom_field_update'),
    path('custom_field/<int:pk>/delete/', views.CustomFieldDelete.as_view(), name='custom_field_delete'),

    # devices
    path('device/create/', views.DeviceCreate.as_view(), name='device_create'),
    path('device/<int:pk>/update/', views.DeviceUpdate.as_view(), name='device_update'),
    path('device/<int:pk>/update_details/', views.device_update_details, name='device_update_details'),
    path('device/<int:pk>/delete/', views.DeviceDelete.as_view(), name='device_delete'),
    path('device/<int:pk>/', views.device_show, name='device_show'),

    # device photos
    path('photo/', views.DevicePhotoListView.as_view(), name='photo_list'),
    path('photo/create/', views.DevicePhotoCreate.as_view(), name='photo_create'),
    path('photo/<int:pk>/', views.DevicePhotoUpdate.as_view(), name='photo_update'),
    path('photo/<int:pk>/delete/', views.DevicePhotoDelete.as_view(), name='photo_delete'),
]
