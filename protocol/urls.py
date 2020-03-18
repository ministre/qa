from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProtocolListView.as_view(), name='protocols'),
    path('<int:device_id>/create/', views.ProtocolCreate.as_view(), name='protocol_create'),
]
