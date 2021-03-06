from django.urls import path
from . import views

urlpatterns = [
    path('', views.FeatureListListView.as_view(), name='fls'),
    path('create/<int:dt_id>', views.FeatureListCreate.as_view(), name='fl_create'),
    path('update/<int:pk>/', views.FeatureListUpdate.as_view(), name='fl_update'),
    path('delete/<int:pk>/', views.FeatureListDelete.as_view(), name='fl_delete'),
    path('<int:pk>/<int:tab_id>/', views.fl_details, name='fl_details'),
    path('clone/<int:pk>/', views.fl_clone, name='fl_clone'),
    path('clear_fli/<int:fl_id>/', views.clear_fli, name='clear_fli'),
    path('category/create/<int:fl_id>/', views.FeatureListCategoryCreate.as_view(), name='fl_category_create'),
    path('category/update/<int:pk>/', views.FeatureListCategoryUpdate.as_view(), name='fl_category_update'),
    path('category/delete/<int:pk>/', views.FeatureListCategoryDelete.as_view(), name='fl_category_delete'),
    path('file/create/<int:fl_id>/', views.FeatureListFileCreate.as_view(), name='fl_file_create'),
    path('file/update/<int:pk>/', views.FeatureListFileUpdate.as_view(), name='fl_file_update'),
    path('file/delete/<int:pk>/', views.FeatureListFileDelete.as_view(), name='fl_file_delete'),
    path('link/create/<int:fl_id>/', views.FeatureListLinkCreate.as_view(), name='fl_link_create'),
    path('link/update/<int:pk>/', views.FeatureListLinkUpdate.as_view(), name='fl_link_update'),
    path('link/delete/<int:pk>/', views.FeatureListLinkDelete.as_view(), name='fl_link_delete'),
    path('item/create/<int:category_id>/', views.FeatureListItemCreate.as_view(), name='fli_create'),
    path('item/update/<int:pk>/', views.FeatureListItemUpdate.as_view(), name='fli_update'),
    path('item/delete/<int:pk>/', views.FeatureListItemDelete.as_view(), name='fli_delete'),
]
