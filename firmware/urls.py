from django.urls import path
from . import views

urlpatterns = [
    path('<int:device_id>/create/', views.FirmwareCreate.as_view(), name='firmware_create'),
    path('<int:device_id>/update/<int:pk>/', views.FirmwareUpdate.as_view(), name='firmware_update'),
    path('<int:device_id>/delete/<int:pk>', views.FirmwareDelete.as_view(), name='firmware_delete'),
]
