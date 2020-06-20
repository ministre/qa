from django.urls import path
from . import views

urlpatterns = [
    path('build_testplan/', views.build_testplan, name='build_testplan'),
]
