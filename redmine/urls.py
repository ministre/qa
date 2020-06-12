from django.urls import path
from . import views

urlpatterns = [
    path('export_test/', views.export_test, name='export_test'),
    path('import_test/', views.import_test, name='import_test'),
    path('export_testplan/', views.export_testplan, name='export_testplan'),
    path('import_testplan/', views.import_testplan, name='import_testplan'),
    path('export_chapter/', views.export_chapter, name='export_chapter'),
    path('import_chapter/', views.import_chapter, name='import_chapter'),
    path('export_fl/', views.export_fl, name='export_fl'),
    path('import_fl/', views.import_fl, name='import_fl'),
]
