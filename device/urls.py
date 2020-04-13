from django.urls import path
from . import views

urlpatterns = [
    path('', views.DeviceListView.as_view(), name='devices'),

    # device types
    path('type/', views.DeviceTypeListView.as_view(), name='device_types'),
    path('type/create/', views.DeviceTypeCreate.as_view(), name='device_type_create'),
    path('type/details/<int:pk>/<int:tab_id>/', views.device_type_details, name='device_type_details'),
    path('type/update/<int:pk>/', views.DeviceTypeUpdate.as_view(), name='device_type_update'),
    path('type/delete/<int:pk>/', views.DeviceTypeDelete.as_view(), name='device_type_delete'),

    # device vendors
    path('vendor/', views.VendorListView.as_view(), name='vendors'),
    path('vendor/create/', views.VendorCreate.as_view(), name='vendor_create'),
    path('vendor/<int:pk>/', views.VendorUpdate.as_view(), name='vendor_update'),
    path('vendor/<int:pk>/delete/', views.VendorDelete.as_view(), name='vendor_delete'),

    # custom fields
    path('custom_field/', views.CustomFieldListView.as_view(), name='custom_fields'),
    path('custom_field/create/', views.CustomFieldCreate.as_view(), name='custom_field_create'),
    path('custom_field/update/<int:pk>/', views.CustomFieldUpdate.as_view(), name='custom_field_update'),
    path('custom_field/<int:pk>/', views.custom_field_details, name='custom_field_details'),
    path('custom_field/<int:pk>/delete/', views.CustomFieldDelete.as_view(), name='custom_field_delete'),
    path('custom_field/<int:custom_field_id>/item/create/',
         views.CustomFieldItemCreate.as_view(), name='custom_field_item_create'),
    path('custom_field/<int:custom_field_id>/item/<int:pk>/delete/',
         views.CustomFieldItemDelete.as_view(), name='custom_field_item_delete'),
    path('custom_field/<int:custom_field_id>/item/<int:pk>/update/',
         views.CustomFieldItemUpdate.as_view(), name='custom_field_item_update'),

    # devices
    path('create/', views.DeviceCreate.as_view(), name='device_create'),
    path('<int:pk>/update/', views.DeviceUpdate.as_view(), name='device_update'),
    path('<int:pk>/update_spec/', views.device_update_spec, name='device_update_spec'),
    path('<int:pk>/delete/', views.DeviceDelete.as_view(), name='device_delete'),
    path('<int:pk>/', views.device_details, name='device_details'),

    # photos
    path('photo/<int:device_id>/create/', views.DevicePhotoCreate.as_view(), name='photo_create'),
    path('photo/<int:device_id>/update/<int:pk>/', views.DevicePhotoUpdate.as_view(), name='photo_update'),
    path('photo/<int:device_id>/delete/<int:pk>/', views.DevicePhotoDelete.as_view(), name='photo_delete'),

    # samples
    path('sample/<int:device_id>/create/', views.SampleCreate.as_view(), name='sample_create'),
    path('sample/<int:device_id>/update/<int:pk>/', views.SampleUpdate.as_view(), name='sample_update'),
    path('sample/<int:device_id>/delete/<int:pk>/', views.SampleDelete.as_view(), name='sample_delete'),
]
