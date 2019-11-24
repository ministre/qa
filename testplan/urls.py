from django.urls import path
from . import views

urlpatterns = [
    path('', views.TestplanListView.as_view(), name='testplans'),
    path('create/', views.TestplanCreate.as_view(), name='testplan_create'),
    path('delete/<int:pk>/', views.TestplanDelete.as_view(), name='testplan_delete'),
    path('update/<int:pk>/', views.TestplanUpdate.as_view(), name='testplan_update'),
    path('<int:testplan_id>/', views.testplan_details, name='testplan_details'),

    # categories
    path('<int:testplan_id>/category/create/', views.CategoryCreate.as_view(), name='category_create'),
    path('<int:testplan_id>/category/<int:pk>/delete/', views.CategoryDelete.as_view(), name='category_delete'),
    path('<int:testplan_id>/category/<int:pk>/update/', views.CategoryUpdate.as_view(), name='category_update'),

    # tests
    path('<int:testplan_id>/category/<int:category_id>/test/create/', views.TestCreate.as_view(), name='test_create'),
    path('<int:testplan_id>/test/<int:pk>/delete/', views.TestDelete.as_view(), name='test_delete'),
    path('<int:testplan_id>/test/<int:pk>/update/', views.TestUpdate.as_view(), name='test_update'),
    path('<int:testplan_id>/test/<int:test_id>/', views.test_details, name='test_details'),
    path('<int:testplan_id>/test/clear_all/', views.clear_tests, name='test_clear_all'),

    # chapters
    path('<int:testplan_id>/chapter/create/', views.ChapterCreate.as_view(), name='chapter_create'),
    path('<int:testplan_id>/chapter/<int:pk>/delete/', views.ChapterDelete.as_view(), name='chapter_delete'),
    path('<int:testplan_id>/chapter/<int:pk>/update/', views.ChapterUpdate.as_view(), name='chapter_update'),
    path('<int:testplan_id>/chapter/<int:pk>/', views.chapter_details, name='chapter_details'),
    path('<int:testplan_id>/chapter/clear_all/', views.clear_chapters, name='chapter_clear_all'),

    # configs
    path('<int:testplan_id>/test/<int:test_id>/config/create/',
         views.TestConfigCreate.as_view(), name='test_config_create'),
    path('<int:testplan_id>/test/<int:test_id>/config/<int:pk>/delete/',
         views.TestConfigDelete.as_view(), name='test_config_delete'),
    path('<int:testplan_id>/test/<int:test_id>/config/<int:pk>/update/',
         views.TestConfigUpdate.as_view(), name='test_config_update'),

    # images
    path('<int:testplan_id>/test/<int:test_id>/image/create/',
         views.TestImageCreate.as_view(), name='test_image_create'),
    path('<int:testplan_id>/test/<int:test_id>/image/<int:pk>/delete/',
         views.TestImageDelete.as_view(), name='test_image_delete'),
    path('<int:testplan_id>/test/<int:test_id>/image/<int:pk>/update/',
         views.TestImageUpdate.as_view(), name='test_image_update'),

    # files
    path('<int:testplan_id>/test/<int:test_id>/file/create/',
         views.TestFileCreate.as_view(), name='test_file_create'),
    path('<int:testplan_id>/test/<int:test_id>/file/<int:pk>/delete/',
         views.TestFileDelete.as_view(), name='test_file_delete'),
    path('<int:testplan_id>/test/<int:test_id>/file/<int:pk>/update/',
         views.TestFileUpdate.as_view(), name='test_file_update'),

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
