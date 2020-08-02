from django.urls import path
from . import views

urlpatterns = [
    # pattern
    path('', views.PatternListView.as_view(), name='patterns'),
    path('create/', views.PatternCreate.as_view(), name='pattern_create'),
    path('update/<int:pk>/', views.PatternUpdate.as_view(), name='pattern_update'),
    path('delete/<int:pk>/', views.PatternDelete.as_view(), name='pattern_delete'),
    path('<int:pk>/<int:tab_id>/', views.pattern_details, name='pattern_details'),
    # category
    path('category/create/<int:p_id>/', views.PatternCategoryCreate.as_view(), name='p_category_create'),
    path('category/update/<int:pk>/', views.PatternCategoryUpdate.as_view(), name='p_category_update'),
    path('category/delete/<int:pk>/', views.PatternCategoryDelete.as_view(), name='p_category_delete'),
    path('category/<int:pk>/<int:tab_id>/', views.p_category_details, name='p_category_details'),
    path('category/up/<int:pk>/', views.p_category_up, name='p_category_up'),
    path('category/down/<int:pk>/', views.p_category_down, name='p_category_down'),
]
