from django.urls import path
from . import views

urlpatterns = [
    path('import_testplan/', views.import_testplan, name='import_testplan'),
    path('import_test_details/', views.import_test_details, name='import_test_details'),
    path('tests_import/', views.tests_import, name='tests_import'),
]
