from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProtocolListView.as_view(), name='protocols'),
    path('<int:pk>/', views.protocol_details, name='protocol_details'),
    path('<int:device_id>/create/', views.ProtocolCreate.as_view(), name='protocol_create'),
    path('<int:device_id>/update/<int:pk>/', views.ProtocolUpdate.as_view(), name='protocol_update'),
    path('<int:device_id>/delete/<int:pk>/', views.ProtocolDelete.as_view(), name='protocol_delete'),

    # branches
    path('branches/', views.BranchListView.as_view(), name='branches'),

]
