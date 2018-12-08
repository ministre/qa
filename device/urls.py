from django.urls import path
from . import views

urlpatterns = [
    path('', views.type_list, name='type_list'),
]
