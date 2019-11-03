from django.urls import path
from . import views

urlpatterns = [
    path('', views.TestplanListView.as_view(), name='testplan_list'),
    path('<int:pk>/', views.testplan_details, name='testplan_details'),
    path('update/<int:pk>/', views.TestplanUpdate.as_view(), name='testplan_update'),
    path('delete/<int:pk>/', views.TestplanDelete.as_view(), name='testplan_delete'),
    path('create/', views.TestplanCreate.as_view(), name='testplan_create'),

    path('<int:pk>/category/create/', views.TestplanCategoryCreate.as_view(), name='testplan_category_create'),
    path('<int:testplan>/category/update/<int:pk>/', views.TestplanCategoryUpdate.as_view(),
         name='testplan_category_update'),
    path('<int:testplan>/category/delete/<int:pk>/', views.TestplanCategoryDelete.as_view(),
         name='testplan_category_delete'),

    path('<int:pk>/chapter/create/', views.TestplanChapterCreate.as_view(), name='testplan_chapter_create'),
    path('<int:testplan>/chapter/update/<int:pk>/', views.TestplanChapterUpdate.as_view(),
         name='testplan_chapter_update'),
    path('<int:testplan>/chapter/delete/<int:pk>/', views.TestplanChapterDelete.as_view(),
         name='testplan_chapter_delete'),

    path('<int:testplan_id>/category/<int:pk>/test/create/', views.TestCreate.as_view(), name='test_create'),
    path('test/<int:pk>/', views.test_details, name='test_details'),
    path('<int:testplan_id>/category/<int:category_id>/test/<int:pk>/update/', views.TestUpdate.as_view(),
         name='test_update'),
    path('<int:testplan>/test/delete/<int:pk>/', views.TestDelete.as_view(), name='test_delete'),

    path('checklist/', views.TestplanChecklistListView.as_view(), name='testplan_checklist_list'),
]
