from django.urls import path
from . import views

urlpatterns = [
    path('import_testplan/', views.import_testplan, name='import_testplan'),
    path('test_details_update/', views.test_details_update, name='test_details_update'),
    path('tests_import/', views.tests_import, name='tests_import'),
]
