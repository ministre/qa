from django.urls import path
from . import views

urlpatterns = [
    path('import_testplan/', views.import_testplan, name='import_testplan'),
    path('import_test_details/', views.import_test_details, name='import_test_details'),
    path('import_all_tests/', views.import_all_tests, name='import_all_tests'),
    path('import_chapter_details/', views.import_chapter_details, name='import_chapter_details'),
    path('import_all_chapters/', views.import_all_chapters, name='import_all_chapters'),
    path('export_device_type/', views.export_device_type, name='export_device_type'),
    path('export_device/', views.export_device, name='export_device'),
]
