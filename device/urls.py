from django.urls import path
from . import views

urlpatterns = [
    path('', views.device_list, name='device_list'),
    path('type/', views.type_list, name='type_list'),
]
