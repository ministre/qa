from django.urls import path
from . import views

urlpatterns = [
    path('', views.TestplanListView.as_view(), name='testplans'),
    path('create/', views.TestplanCreate.as_view(), name='testplan_create'),
    path('delete/<int:pk>/', views.TestplanDelete.as_view(), name='testplan_delete'),
    path('update/<int:pk>/', views.TestplanUpdate.as_view(), name='testplan_update'),
    path('<int:pk>/', views.testplan_details, name='testplan_details'),

    path('<int:testplan>/category/create/', views.CategoryCreate.as_view(), name='category_create'),
    path('<int:testplan>/category/delete/<int:pk>/', views.CategoryDelete.as_view(), name='category_delete'),
    path('<int:testplan>/category/update/<int:pk>/', views.CategoryUpdate.as_view(), name='category_update'),

    path('<int:testplan>/test/create/<int:pk>/', views.TestCreate.as_view(), name='test_create'),
    path('<int:testplan>/test/delete/<int:pk>/', views.TestDelete.as_view(), name='test_delete'),
    path('<int:testplan>/test/update/<int:pk>/', views.TestUpdate.as_view(), name='test_update'),
    path('<int:testplan_id>/test/<int:test_id>/', views.test_details, name='test_details'),
    path('<int:testplan>/clear_tests/', views.clear_tests, name='clear_tests'),

    path('<int:testplan>/chapter/create/', views.ChapterCreate.as_view(), name='chapter_create'),
    path('<int:testplan>/chapter/delete/<int:pk>/', views.ChapterDelete.as_view(), name='chapter_delete'),
    path('<int:testplan>/chapter/update/<int:pk>/', views.ChapterUpdate.as_view(), name='chapter_update'),
    path('<int:testplan>/chapter/<int:pk>/', views.chapter_details, name='chapter_details'),
    path('<int:testplan>/clear_chapters/', views.clear_chapters, name='clear_chapters'),

    path('<int:testplan>/config/create/<int:pk>/', views.TestConfigCreate.as_view(), name='test_config_create'),
    path('<int:testplan>/test/<int:test>/config/delete/<int:pk>/', views.TestConfigDelete.as_view(),
         name='test_config_delete'),
    path('<int:testplan>/test/<int:test>/config/update/<int:pk>/', views.TestConfigUpdate.as_view(),
         name='test_config_update'),

    path('<int:testplan>/image/create/<int:pk>/', views.TestImageCreate.as_view(), name='test_image_create'),
    path('<int:testplan>/test/<int:test>/image/delete/<int:pk>/', views.TestImageDelete.as_view(),
         name='test_image_delete'),
    path('<int:testplan>/test/<int:test>/image/update/<int:pk>/', views.TestImageUpdate.as_view(),
         name='test_image_update'),

    path('<int:testplan>/file/create/<int:pk>/', views.TestFileCreate.as_view(), name='test_file_create'),
    path('<int:testplan>/test/<int:test>/file/delete/<int:pk>/', views.TestFileDelete.as_view(),
         name='test_file_delete'),
    path('<int:testplan>/test/<int:test>/file/update/<int:pk>/', views.TestFileUpdate.as_view(),
         name='test_file_update'),

    # checklists
    path('<int:testplan_id>/test/<int:test_id>/checklist/create/',
         views.TestChecklistCreate.as_view(), name='test_checklist_create'),
    path('<int:testplan_id>/test/<int:test_id>/checklist/<int:pk>/delete/',
         views.TestChecklistDelete.as_view(), name='test_checklist_delete'),
    path('<int:testplan_id>/test/<int:test_id>/checklist/<int:pk>/update/',
         views.TestChecklistUpdate.as_view(), name='test_checklist_update'),

    # checklist items
    path('<int:testplan_id>/test/<int:test_id>/checklist/<int:checklist_id>/item/create/',
         views.ChecklistItemCreate.as_view(), name='checklist_item_create'),

    # links
    path('<int:testplan_id>/test/<int:test_id>/link/create/',
         views.TestLinkCreate.as_view(), name='test_link_create'),
    path('<int:testplan_id>/test/<int:test_id>/link/<int:pk>/delete/',
         views.TestLinkDelete.as_view(), name='test_link_delete'),
    path('<int:testplan_id>/test/<int:test_id>/link/<int:pk>/update/',
         views.TestLinkUpdate.as_view(), name='test_link_update'),

    # patterns
    path('pattern/', views.PatternListView.as_view(), name='patterns'),
    path('pattern/create/', views.PatternCreate.as_view(), name='pattern_create'),
]
