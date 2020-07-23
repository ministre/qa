from django.urls import path
from . import views

urlpatterns = [
    path('', views.DeviceListView.as_view(), name='devices'),

    # vendors
    path('vendors/', views.VendorListView.as_view(), name='vendors'),
    path('vendor/create/', views.VendorCreate.as_view(), name='vendor_create'),
    path('vendor/update/<int:pk>/', views.VendorUpdate.as_view(), name='vendor_update'),
    path('vendor/delete/<int:pk>/', views.VendorDelete.as_view(), name='vendor_delete'),
    path('vendor/<int:pk>/', views.vendor_details, name='vendor_details'),

    # checklists
    path('checklists/', views.DeviceChecklistListView.as_view(), name='d_checklists'),
    path('checklist/create/', views.DeviceChecklistCreate.as_view(), name='d_checklist_create'),
    path('checklist/update/<int:pk>/', views.DeviceChecklistUpdate.as_view(), name='d_checklist_update'),
    path('checklist/delete/<int:pk>/', views.DeviceChecklistDelete.as_view(), name='d_checklist_delete'),
    path('checklist/<int:pk>/<int:tab_id>/', views.device_checklist_details, name='d_checklist_details'),

    # checklist items
    path('checklist/item/create/<int:cl_id>/', views.DeviceChecklistItemCreate.as_view(), name='d_cl_item_create'),
    path('checklist/item/update/<int:pk>/', views.DeviceChecklistItemUpdate.as_view(), name='d_cl_item_update'),
    path('checklist/item/delete/<int:pk>/', views.DeviceChecklistItemDelete.as_view(), name='d_cl_item_delete'),

    # selectable value list
    path('slists/', views.DeviceSlistListView.as_view(), name='d_slists'),
    path('slist/create/', views.DeviceSlistCreate.as_view(), name='d_slist_create'),
    path('slist/update/<int:pk>/', views.DeviceSlistUpdate.as_view(), name='d_slist_update'),
    path('slist/delete/<int:pk>/', views.DeviceSlistDelete.as_view(), name='d_slist_delete'),
    path('slist/<int:pk>/<int:tab_id>/', views.device_slist_details, name='d_slist_details'),

    # selectable value items
    path('slist/item/create/<int:sl_id>/', views.DeviceSlistItemCreate.as_view(), name='d_sl_item_create'),
    path('slist/item/update/<int:pk>/', views.DeviceSlistItemUpdate.as_view(), name='d_sl_item_update'),
    path('slist/item/delete/<int:pk>/', views.DeviceSlistItemDelete.as_view(), name='d_sl_item_delete'),

    # text field
    path('tfs/', views.DeviceTextFieldListView.as_view(), name='d_tfields'),
    path('tf/create/', views.DeviceTextFieldCreate.as_view(), name='d_tf_create'),
    path('tf/update/<int:pk>/', views.DeviceTextFieldUpdate.as_view(), name='d_tf_update'),
    path('tf/delete/<int:pk>/', views.DeviceTextFieldDelete.as_view(), name='d_tf_delete'),
    path('tf/<int:pk>/', views.device_tf_details, name='d_tf_details'),

    # integer field
    path('ifs/', views.DeviceIntegerFieldListView.as_view(), name='d_ifields'),
    path('if/create/', views.DeviceIntegerFieldCreate.as_view(), name='d_if_create'),
    path('if/update/<int:pk>/', views.DeviceIntegerFieldUpdate.as_view(), name='d_if_update'),
    path('if/delete/<int:pk>/', views.DeviceIntegerFieldDelete.as_view(), name='d_if_delete'),
    path('if/<int:pk>/', views.device_if_details, name='d_if_details'),

    # device types
    path('type/', views.DeviceTypeListView.as_view(), name='device_types'),
    path('type/create/', views.DeviceTypeCreate.as_view(), name='device_type_create'),
    path('type/details/<int:pk>/<int:tab_id>/', views.device_type_details, name='device_type_details'),
    path('type/update/<int:pk>/', views.DeviceTypeUpdate.as_view(), name='device_type_update'),
    path('type/delete/<int:pk>/', views.DeviceTypeDelete.as_view(), name='device_type_delete'),

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
    path('details/<int:pk>/<int:tab_id>/', views.device_details, name='device_details'),

    # photos
    path('photo/<int:device_id>/create/', views.DevicePhotoCreate.as_view(), name='photo_create'),
    path('photo/<int:device_id>/update/<int:pk>/', views.DevicePhotoUpdate.as_view(), name='photo_update'),
    path('photo/<int:device_id>/delete/<int:pk>/', views.DevicePhotoDelete.as_view(), name='photo_delete'),

    # samples
    path('sample/<int:device_id>/create/', views.SampleCreate.as_view(), name='sample_create'),
    path('sample/<int:device_id>/update/<int:pk>/', views.SampleUpdate.as_view(), name='sample_update'),
    path('sample/<int:device_id>/delete/<int:pk>/', views.SampleDelete.as_view(), name='sample_delete'),
]
