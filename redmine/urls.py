from django.urls import path
from . import views

urlpatterns = [
    path('export_test/', views.export_test, name='export_test'),
    path('import_test/', views.import_test, name='import_test'),

    path('export_testplan/', views.export_testplan, name='export_testplan'),
    path('import_testplan/', views.import_testplan, name='import_testplan'),

#    path('import_p_test_details/', views.import_p_test_details, name='import_p_test_details'),
#    path('import_all_tests/', views.import_all_tests, name='import_all_tests'),
#    path('import_chapter_details/', views.import_chapter_details, name='import_chapter_details'),
#    path('import_all_chapters/', views.import_all_chapters, name='import_all_chapters'),
#    path('export_device_type/', views.export_device_type, name='export_device_type'),
#    path('export_device/', views.export_device, name='export_device'),
#    path('export_pattern/', views.export_pattern, name='export_pattern'),
]
