from django.urls import path
from . import views

urlpatterns = [
    path('testplan_import/', views.testplan_import, name='testplan_import'),
    path('test_details_update/', views.test_details_update, name='test_details_update'),
]
