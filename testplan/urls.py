from django.urls import path
from . import views

urlpatterns = [
    # testplan
    path('<int:tab_id>/', views.testplan_list, name='testplans'),
    path('t/create/', views.TestplanCreate.as_view(), name='testplan_create'),
    path('t/delete/<int:pk>/', views.TestplanDelete.as_view(), name='testplan_delete'),
    path('t/update/<int:pk>/', views.TestplanUpdate.as_view(), name='testplan_update'),
    path('t/<int:pk>/<int:tab_id>/', views.testplan_details, name='testplan_details'),
    path('t/clone/<int:pk>/', views.testplan_clone, name='testplan_clone'),
    # pattern
    path('p/create/', views.PatternCreate.as_view(), name='pattern_create'),
    path('p/delete/<int:pk>/', views.PatternDelete.as_view(), name='pattern_delete'),
    path('p/update/<int:pk>/', views.PatternUpdate.as_view(), name='pattern_update'),
    path('p/<int:pk>/<int:tab_id>/', views.pattern_details, name='pattern_details'),
    # chapters
    path('chapter/create/<int:tp_id>/', views.ChapterCreate.as_view(), name='chapter_create'),
    path('chapter/delete/<int:pk>/', views.ChapterDelete.as_view(), name='chapter_delete'),
    path('chapter/update/<int:pk>/', views.ChapterUpdate.as_view(), name='chapter_update'),
    path('chapter/<int:pk>/', views.chapter_details, name='chapter_details'),
    path('clear_chapters/<int:tp_id>/', views.clear_chapters, name='clear_chapters'),
    # categories
    path('<int:testplan_id>/category/create/', views.CategoryCreate.as_view(), name='category_create'),
    path('<int:testplan_id>/category/<int:pk>/delete/', views.CategoryDelete.as_view(), name='category_delete'),
    path('<int:testplan_id>/category/<int:pk>/update/', views.CategoryUpdate.as_view(), name='category_update'),
    # tests
    path('test/create/<int:category_id>/', views.TestCreate.as_view(), name='test_create'),
    path('test/delete/<int:pk>/', views.TestDelete.as_view(), name='test_delete'),
    path('test/update/<int:pk>/', views.TestUpdate.as_view(), name='test_update'),
    path('test/<int:pk>/<int:tab_id>/', views.test_details, name='test_details'),
    path('clear_tests/<int:tp_id>/', views.clear_tests, name='clear_tests'),
    # configs
    path('test_config/create/<int:test_id>/', views.TestConfigCreate.as_view(), name='test_config_create'),
    path('test_config/delete/<int:pk>/', views.TestConfigDelete.as_view(), name='test_config_delete'),
    path('test_config/update/<int:pk>/', views.TestConfigUpdate.as_view(), name='test_config_update'),
    # images
    path('test_image/create/<int:test_id>/', views.TestImageCreate.as_view(), name='test_image_create'),
    path('test_image/delete/<int:pk>/', views.TestImageDelete.as_view(), name='test_image_delete'),
    path('test_image/update/<int:pk>/', views.TestImageUpdate.as_view(), name='test_image_update'),
    # files
    path('test_file/create/<int:test_id>/', views.TestFileCreate.as_view(), name='test_file_create'),
    path('test_file/delete/<int:pk>/', views.TestFileDelete.as_view(), name='test_file_delete'),
    path('test_file/update/<int:pk>/', views.TestFileUpdate.as_view(), name='test_file_update'),

    # checklists
    path('checklist/create/<int:test_id>/', views.TestChecklistCreate.as_view(), name='test_checklist_create'),

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
    path('test_link/create/<int:test_id>/', views.TestLinkCreate.as_view(), name='test_link_create'),
    path('test_link/delete/<int:pk>/', views.TestLinkDelete.as_view(), name='test_link_delete'),
    path('test_link/update/<int:pk>/', views.TestLinkUpdate.as_view(), name='test_link_update'),
    # comments
    path('test_comment/create/<int:test_id>/', views.TestCommentCreate.as_view(), name='test_comment_create'),
    path('test_comment/delete/<int:pk>/', views.TestCommentDelete.as_view(), name='test_comment_delete'),
    path('test_comment/update/<int:pk>/', views.TestCommentUpdate.as_view(), name='test_comment_update'),
]