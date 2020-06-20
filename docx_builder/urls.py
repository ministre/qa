from django.urls import path
from . import views

urlpatterns = [
    path('', views.DocxProfileListView.as_view(), name='docx_profiles'),
    path('create/', views.DocxProfileCreate.as_view(), name='docx_profile_create'),
    path('<int:pk>/', views.docx_profile_details, name='docx_profile_details'),
    path('build_testplan/', views.build_testplan, name='build_testplan'),
]
