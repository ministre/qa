from django.urls import path
from . import views

urlpatterns = [
    path('', views.DocxProfileListView.as_view(), name='docx_profiles'),
    path('create/', views.DocxProfileCreate.as_view(), name='docx_profile_create'),
    path('update/<int:pk>/', views.DocxProfileUpdate.as_view(), name='docx_profile_update'),
    path('delete/<int:pk>/', views.DocxProfileDelete.as_view(), name='docx_profile_delete'),
    path('build_testplan/', views.build_testplan, name='build_testplan'),
]
