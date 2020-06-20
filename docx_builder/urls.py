from django.urls import path
from . import views

urlpatterns = [
    path('', views.DocxProfileListView.as_view(), name='docx_profiles'),
    path('<int:pk>/', views.docx_profile_details, name='docx_profile_details'),
    path('build_testplan/', views.build_testplan, name='build_testplan'),
]
