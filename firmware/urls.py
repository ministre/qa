from django.urls import path
from . import views

urlpatterns = [
    path('', views.FirmwareListView.as_view(), name='firmwares'),
    path('create/', views.FirmwareCreate.as_view(), name='firmware_create'),
    path('<int:pk>/', views.FirmwareUpdate.as_view(), name='firmware_update'),
    path('<int:pk>/delete/', views.FirmwareDelete.as_view(), name='firmware_delete'),
]
