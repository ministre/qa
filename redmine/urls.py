from django.urls import path
from . import views

urlpatterns = [
    path('testplan/import/', views.redmine_testplan_import, name='redmine_testplan_import'),
    path('test/<int:pk>/import/', views.redmine_test_import, name='redmine_test_import'),
]
