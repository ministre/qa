from django.urls import path
from . import views

urlpatterns = [
    # Feature List
    path('', views.FeatureListListView.as_view(), name='feature_lists'),
    path('create/', views.FeatureListCreate.as_view(), name='feature_list_create'),
    path('<int:pk>/update/', views.FeatureListUpdate.as_view(), name='feature_list_update'),
    path('<int:pk>/delete/', views.FeatureListDelete.as_view(), name='feature_list_delete'),
    path('<int:pk>/', views.feature_list_details, name='feature_list_details'),
    # Feature List Categories
    path('<int:feature_list_id>/category/create/', views.FeatureListCategoryCreate.as_view(),
         name='feature_list_category_create'),
    path('<int:feature_list_id>/category/<int:pk>/delete/', views.FeatureListCategoryDelete.as_view(),
         name='feature_list_category_delete'),
    path('<int:feature_list_id>/category/<int:pk>/update/', views.FeatureListCategoryUpdate.as_view(),
         name='feature_list_category_update'),
]
