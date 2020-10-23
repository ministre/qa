from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProtocolListView.as_view(), name='protocols'),

    # protocols
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
    path('device/sample/update/<int:pk>/', views.ProtocolDeviceSampleUpdate.as_view(),
         name='protocol_device_sample_update'),
    path('device/delete/<int:pk>/', views.ProtocolDeviceDelete.as_view(), name='protocol_device_delete'),

    # protocol files
    path('scan/create/<int:p_id>/', views.ProtocolScanCreate.as_view(), name='protocol_scan_create'),
    path('scan/update/<int:pk>/', views.ProtocolScanUpdate.as_view(), name='protocol_scan_update'),
    path('scan/delete/<int:pk>/', views.ProtocolScanDelete.as_view(), name='protocol_scan_delete'),

    # test results
    path('test/result/create/<int:protocol_id>/<int:test_id>/', views.protocol_test_result_create,
         name='protocol_test_result_create'),
    path('test/result/details/<int:pk>/<int:tab_id>/', views.protocol_test_result_details,
         name='protocol_test_result_details'),
    path('test/result/delete/<int:pk>/', views.ProtocolTestResultDelete.as_view(),
         name='protocol_test_result_delete'),

    # test result issues
    path('test/result/issue/create/<int:tr>/', views.TestResultIssueCreate.as_view(), name='test_result_issue_create'),
    path('test/result/issue/update/<int:pk>/', views.TestResultIssueUpdate.as_view(), name='test_result_issue_update'),
    path('test/result/issue/delete/<int:pk>/', views.TestResultIssueDelete.as_view(), name='test_result_issue_delete'),

    # test result comments
    path('test/result/comment/create/<int:tr>/', views.TestResultCommentCreate.as_view(),
         name='test_result_comment_create'),
    path('test/result/comment/update/<int:pk>/', views.TestResultCommentUpdate.as_view(),
         name='test_result_comment_update'),
    path('test/result/comment/delete/<int:pk>/', views.TestResultCommentDelete.as_view(),
         name='test_result_comment_delete'),
]
