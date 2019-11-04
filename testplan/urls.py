from django.urls import path
from . import views

urlpatterns = [
    path('', views.TestplanListView.as_view(), name='testplan_list'),
    path('create/', views.TestplanCreate.as_view(), name='testplan_create'),
    path('update/<int:pk>/', views.TestplanUpdate.as_view(), name='testplan_update'),
    path('delete/<int:pk>/', views.TestplanDelete.as_view(), name='testplan_delete'),
    path('<int:pk>/', views.testplan_details, name='testplan_details'),

    path('<int:testplan>/category/create/', views.CategoryCreate.as_view(), name='category_create'),
    path('<int:testplan>/category/update/<int:pk>/', views.CategoryUpdate.as_view(), name='category_update'),
    path('<int:testplan>/category/delete/<int:pk>/', views.CategoryDelete.as_view(), name='category_delete'),

    path('<int:testplan>/test/create/<int:pk>/', views.TestCreate.as_view(), name='test_create'),
    path('<int:testplan>/test/update/<int:pk>/', views.TestUpdate.as_view(), name='test_update'),
    path('<int:testplan>/test/delete/<int:pk>/', views.TestDelete.as_view(), name='test_delete'),
    path('<int:testplan>/test/details/<int:pk>/', views.test_details, name='test_details'),

    path('<int:pk>/chapter/create/', views.TestplanChapterCreate.as_view(), name='testplan_chapter_create'),
    path('<int:testplan>/chapter/update/<int:pk>/', views.TestplanChapterUpdate.as_view(),
         name='testplan_chapter_update'),
    path('<int:testplan>/chapter/delete/<int:pk>/', views.TestplanChapterDelete.as_view(),
         name='testplan_chapter_delete'),

    path('checklist/', views.TestplanChecklistListView.as_view(), name='testplan_checklist_list'),
]
