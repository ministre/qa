from django.urls import path
from . import views

urlpatterns = [
    path('', views.FeatureListListView.as_view(), name='feature_lists'),
    path('create/', views.FeatureListCreate.as_view(), name='feature_list_create'),
    path('<int:pk>/update/', views.FeatureListUpdate.as_view(), name='feature_list_update'),
    path('<int:pk>/delete/', views.FeatureListDelete.as_view(), name='feature_list_delete'),
    path('<int:pk>/', views.feature_list_details, name='feature_list_details'),
]
