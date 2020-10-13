from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProtocolListView.as_view(), name='protocols'),
    path('create/', views.ProtocolCreate.as_view(), name='protocol_create'),
    path('update/<int:pk>/', views.ProtocolUpdate.as_view(), name='protocol_update'),
    path('delete/<int:pk>/', views.ProtocolDelete.as_view(), name='protocol_delete'),
    path('<int:pk>/<int:tab_id>/', views.protocol_details, name='protocol_details'),

    # branches
    path('branches/', views.BranchListView.as_view(), name='branches'),
    path('branch/create/', views.BranchCreate.as_view(), name='branch_create'),
    path('branch/update/<int:pk>/', views.BranchUpdate.as_view(), name='branch_update'),
    path('branch/delete/<int:pk>/', views.BranchDelete.as_view(), name='branch_delete'),

    # protocol devices
    path('device/create/<int:p_id>/', views.ProtocolDeviceCreate.as_view(), name='protocol_device_create'),
    path('device/update/<int:pk>/', views.ProtocolDeviceUpdate.as_view(), name='protocol_device_update'),
    path('device/fw/update/<int:pk>/', views.ProtocolDeviceFwUpdate.as_view(), name='protocol_device_fw_update'),
    path('device/delete/<int:pk>/', views.ProtocolDeviceDelete.as_view(), name='protocol_device_delete'),
]
