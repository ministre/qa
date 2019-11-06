from django.urls import path
from . import views

urlpatterns = [
    path('testplan/', views.make_testplan, name='make_testplan'),
]
