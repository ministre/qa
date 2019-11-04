from django.urls import path
from . import views

urlpatterns = [
    path('import_testplan/', views.import_testplan, name='import_testplan'),
    path('import_test_details/', views.import_test_details, name='import_test_details'),
    path('import_all_tests/', views.import_all_tests, name='import_all_tests'),
]
