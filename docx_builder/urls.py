from django.urls import path
from . import views

urlpatterns = [
    path('build_testplan/<int:tp_id>/', views.build_testplan, name='build_testplan'),
]
