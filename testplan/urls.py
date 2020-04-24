from django.urls import path
from . import views

urlpatterns = [
    path('<int:tab_id>/', views.testplan_list, name='testplans'),
    path('t/<int:pk>/<int:tab_id>/', views.testplan_details, name='testplan_details'),
    path('p/<int:pk>/<int:tab_id>/', views.pattern_details, name='pattern_details'),
    path('t_create/', views.TestplanCreate.as_view(), name='testplan_create'),
    path('p_create/', views.PatternCreate.as_view(), name='pattern_create'),
    path('t_update/<int:pk>/', views.TestplanUpdate.as_view(), name='testplan_update'),
    path('p_update/<int:pk>/', views.PatternUpdate.as_view(), name='pattern_update'),
    path('t_delete/<int:pk>/', views.TestplanDelete.as_view(), name='testplan_delete'),
    path('p_delete/<int:pk>/', views.PatternDelete.as_view(), name='pattern_delete'),

    # categories
    path('<int:testplan_id>/category/create/', views.CategoryCreate.as_view(), name='category_create'),
    path('<int:testplan_id>/category/<int:pk>/delete/', views.CategoryDelete.as_view(), name='category_delete'),
    path('<int:testplan_id>/category/<int:pk>/update/', views.CategoryUpdate.as_view(), name='category_update'),

    # tests
    path('<int:testplan_id>/category/<int:category_id>/test/create/', views.TestCreate.as_view(), name='test_create'),
    path('<int:testplan_id>/test/<int:pk>/delete/', views.TestDelete.as_view(), name='test_delete'),
    path('<int:testplan_id>/test/<int:pk>/update/', views.TestUpdate.as_view(), name='test_update'),
    path('<int:testplan_id>/test/<int:pk>/<int:tab_id>/', views.test_details, name='test_details'),
    path('<int:testplan_id>/clear_tests/', views.clear_tests, name='clear_tests'),

    # chapters
    path('<int:testplan_id>/chapter/create/', views.ChapterCreate.as_view(), name='chapter_create'),
    path('<int:testplan_id>/chapter/<int:pk>/delete/', views.ChapterDelete.as_view(), name='chapter_delete'),
    path('<int:testplan_id>/chapter/<int:pk>/update/', views.ChapterUpdate.as_view(), name='chapter_update'),
    path('<int:testplan_id>/chapter/<int:chapter_id>/', views.chapter_details, name='chapter_details'),
    path('<int:testplan_id>/clear_chapters/', views.clear_chapters, name='clear_chapters'),

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
    path('<int:testplan_id>/test/<int:test_id>/item/<int:pk>/delete/',
         views.ChecklistItemDelete.as_view(), name='checklist_item_delete'),
    path('<int:testplan_id>/test/<int:test_id>/item/<int:pk>/update/',
         views.ChecklistItemUpdate.as_view(), name='checklist_item_update'),

    # worksheets
    path('<int:testplan_id>/test/<int:test_id>/worksheet/create/',
         views.TestWorksheetCreate.as_view(), name='test_worksheet_create'),
    path('<int:testplan_id>/test/<int:test_id>/worksheet/<int:pk>/delete/',
         views.TestWorksheetDelete.as_view(), name='test_worksheet_delete'),
    path('<int:testplan_id>/test/<int:test_id>/worksheet/<int:pk>/update/',
         views.TestWorksheetUpdate.as_view(), name='test_worksheet_update'),

    # worksheet items
    path('<int:testplan_id>/test/<int:test_id>/worksheet/<int:worksheet_id>/item/create/',
         views.WorksheetItemCreate.as_view(), name='worksheet_item_create'),
    path('<int:testplan_id>/test/<int:test_id>/w_item/<int:pk>/delete/',
         views.WorksheetItemDelete.as_view(), name='worksheet_item_delete'),
    path('<int:testplan_id>/test/<int:test_id>/w_item/<int:pk>/update/',
         views.WorksheetItemUpdate.as_view(), name='worksheet_item_update'),

    # links
    path('<int:testplan_id>/test/<int:test_id>/link/create/',
         views.TestLinkCreate.as_view(), name='test_link_create'),
    path('<int:testplan_id>/test/<int:test_id>/link/<int:pk>/delete/',
         views.TestLinkDelete.as_view(), name='test_link_delete'),
    path('<int:testplan_id>/test/<int:test_id>/link/<int:pk>/update/',
         views.TestLinkUpdate.as_view(), name='test_link_update'),

    # comments
    path('<int:testplan_id>/test/<int:test_id>/comment/create/',
         views.TestCommentCreate.as_view(), name='test_comment_create'),
    path('<int:testplan_id>/test/<int:test_id>/comment/<int:pk>/delete/',
         views.TestCommentDelete.as_view(), name='test_comment_delete'),
    path('<int:testplan_id>/test/<int:test_id>/comment/<int:pk>/update/',
         views.TestCommentUpdate.as_view(), name='test_comment_update'),
]
