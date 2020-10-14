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

    # selection lists
    path('slists/', views.DeviceSlistListView.as_view(), name='d_slists'),
    path('slist/create/', views.DeviceSlistCreate.as_view(), name='d_slist_create'),
    path('slist/update/<int:pk>/', views.DeviceSlistUpdate.as_view(), name='d_slist_update'),
    path('slist/delete/<int:pk>/', views.DeviceSlistDelete.as_view(), name='d_slist_delete'),
    path('slist/<int:pk>/<int:tab_id>/', views.device_slist_details, name='d_slist_details'),

    # selection list items
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
    path('types/', views.DeviceTypeListView.as_view(), name='device_types'),
    path('type/create/', views.DeviceTypeCreate.as_view(), name='device_type_create'),
    path('type/update/<int:pk>/', views.DeviceTypeUpdate.as_view(), name='device_type_update'),
    path('type/delete/<int:pk>/', views.DeviceTypeDelete.as_view(), name='device_type_delete'),
    path('type/details/<int:pk>/<int:tab_id>/', views.device_type_details, name='device_type_details'),

    # device type specifications
    path('type/spec/create/<int:dt>/<int:st>/', views.dt_spec_create, name='dt_spec_create'),
    path('type/spec/delete/<int:dt>/<int:pk>/', views.dt_spec_delete, name='dt_spec_delete'),

    # devices
    path('create/', views.DeviceCreate.as_view(), name='device_create'),
    path('<int:pk>/update/', views.DeviceUpdate.as_view(), name='device_update'),
    path('<int:pk>/delete/', views.DeviceDelete.as_view(), name='device_delete'),
    path('details/<int:pk>/<int:tab_id>/', views.device_details, name='device_details'),
    path('spec/update/', views.spec_update, name='spec_update'),

    # device photos
    path('photo/create/<int:d_id>/', views.DevicePhotoCreate.as_view(), name='photo_create'),
    path('photo/update/<int:pk>/', views.DevicePhotoUpdate.as_view(), name='photo_update'),
    path('photo/delete/<int:pk>/', views.DevicePhotoDelete.as_view(), name='photo_delete'),

    # device document types
    path('doc/type/', views.DeviceDocumentTypeListView.as_view(), name='d_doc_types'),
    path('doc/type/create/', views.DeviceDocumentTypeCreate.as_view(), name='d_doc_type_create'),
    path('doc/type/update/<int:pk>/', views.DeviceDocumentTypeUpdate.as_view(), name='d_doc_type_update'),
    path('doc/type/delete/<int:pk>/', views.DeviceDocumentTypeDelete.as_view(), name='d_doc_type_delete'),

    # device documents
    path('doc/create/<int:d_id>/', views.DeviceDocumentCreate.as_view(), name='doc_create'),
    path('doc/update/<int:pk>/', views.DeviceDocumentUpdate.as_view(), name='doc_update'),
    path('doc/delete/<int:pk>/', views.DeviceDocumentDelete.as_view(), name='doc_delete'),

    # device samples
    path('sample/create/<int:d_id>', views.DeviceSampleCreate.as_view(), name='sample_create'),
    path('sample/update/<int:pk>/', views.DeviceSampleUpdate.as_view(), name='sample_update'),
    path('sample/delete/<int:pk>/', views.DeviceSampleDelete.as_view(), name='sample_delete'),
    path('sample/account/create/<int:s_id>', views.DeviceSampleAccountCreate.as_view(), name='sample_account_create'),

    # firmware
    path('fw/create/<int:d_id>/', views.FirmwareCreate.as_view(), name='fw_create'),
    path('fw/update/<int:pk>/', views.FirmwareUpdate.as_view(), name='fw_update'),
    path('fw/delete/<int:pk>/', views.FirmwareDelete.as_view(), name='fw_delete'),
    path('fw/<int:pk>/<int:tab_id>/', views.fw_details, name='fw_details'),

    # firmware account
    path('fw/account/create/<int:fw_id>/', views.FirmwareAccountCreate.as_view(), name='fw_account_create'),
    path('fw/account/update/<int:pk>/', views.FirmwareAccountUpdate.as_view(), name='fw_account_update'),
    path('fw/account/delete/<int:pk>/', views.FirmwareAccountDelete.as_view(), name='fw_account_delete'),

    # firmware file
    path('fw/file/create/<int:fw_id>/', views.FirmwareFileCreate.as_view(), name='fw_file_create'),
    path('fw/file/update/<int:pk>/', views.FirmwareFileUpdate.as_view(), name='fw_file_update'),
    path('fw/file/delete/<int:pk>/', views.FirmwareFileDelete.as_view(), name='fw_file_delete'),

    # firmware screenshot
    path('fw/screenshot/create/<int:fw_id>/', views.FirmwareScreenshotCreate.as_view(), name='fw_screenshot_create'),
    path('fw/screenshot/update/<int:pk>/', views.FirmwareScreenshotUpdate.as_view(), name='fw_screenshot_update'),
    path('fw/screenshot/delete/<int:pk>/', views.FirmwareScreenshotDelete.as_view(), name='fw_screenshot_delete'),

    # firmware howto
    path('fw/howto/create/<int:fw_id>/', views.FirmwareHowtoCreate.as_view(), name='fw_howto_create'),
    path('fw/howto/update/<int:pk>/', views.FirmwareHowtoUpdate.as_view(), name='fw_howto_update'),
    path('fw/howto/delete/<int:pk>/', views.FirmwareHowtoDelete.as_view(), name='fw_howto_delete'),

    # support contact
    path('support/create/<int:d_id>/', views.DeviceSupportCreate.as_view(), name='d_support_create'),
    path('support/delete/<int:pk>/', views.DeviceSupportDelete.as_view(), name='d_support_delete'),
]
