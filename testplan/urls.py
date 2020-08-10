from django.urls import path
from . import views

urlpatterns = [
    # testplan
    path('', views.testplan_list, name='testplans'),
    path('create/', views.TestplanCreate.as_view(), name='testplan_create'),
    path('delete/<int:pk>/', views.TestplanDelete.as_view(), name='testplan_delete'),
    path('update/<int:pk>/', views.TestplanUpdate.as_view(), name='testplan_update'),
    path('<int:pk>/<int:tab_id>/', views.testplan_details, name='testplan_details'),
    path('clone/<int:pk>/', views.testplan_clone, name='testplan_clone'),
    # chapters
    path('chapter/create/<int:tp_id>/', views.ChapterCreate.as_view(), name='chapter_create'),
    path('chapter/delete/<int:pk>/', views.ChapterDelete.as_view(), name='chapter_delete'),
    path('chapter/update/<int:pk>/', views.ChapterUpdate.as_view(), name='chapter_update'),
    path('chapter/<int:pk>/<int:tab_id>/', views.chapter_details, name='chapter_details'),
    path('clear_chapters/<int:tp_id>/', views.clear_chapters, name='clear_chapters'),
    # testplan categories
    path('category/create/<int:t_id>/', views.TestplanCategoryCreate.as_view(), name='t_category_create'),
    path('category/update/<int:pk>/', views.TestplanCategoryUpdate.as_view(), name='t_category_update'),
    path('category/delete/<int:pk>/', views.TestplanCategoryDelete.as_view(), name='t_category_delete'),
    path('category/<int:pk>/<int:tab_id>/', views.t_category_details, name='t_category_details'),
    path('category/up/<int:pk>/', views.t_category_up, name='t_category_up'),
    path('category/down/<int:pk>/', views.t_category_down, name='t_category_down'),
    # tests
    path('test/create/<int:category_id>/', views.TestCreate.as_view(), name='test_create'),
    path('test/delete/<int:pk>/', views.TestDelete.as_view(), name='test_delete'),
    path('test/update/<int:pk>/', views.TestUpdate.as_view(), name='test_update'),
    path('test/move/<int:pk>/', views.t_test_move, name='t_test_move'),
    path('test/copy/<int:pk>/', views.t_test_copy, name='t_test_copy'),
    path('test/<int:pk>/<int:tab_id>/', views.test_details, name='test_details'),
    path('clear_tests/<int:tp_id>/', views.clear_tests, name='clear_tests'),
    path('test/up/<int:pk>/', views.t_test_up, name='t_test_up'),
    path('test/down/<int:pk>/', views.t_test_down, name='t_test_down'),
    # configs
    path('config/create/<int:test_id>/', views.TestConfigCreate.as_view(), name='test_config_create'),
    path('config/delete/<int:pk>/', views.TestConfigDelete.as_view(), name='test_config_delete'),
    path('config/update/<int:pk>/', views.TestConfigUpdate.as_view(), name='test_config_update'),
    # images
    path('image/create/<int:test_id>/', views.TestImageCreate.as_view(), name='test_image_create'),
    path('image/delete/<int:pk>/', views.TestImageDelete.as_view(), name='test_image_delete'),
    path('image/update/<int:pk>/', views.TestImageUpdate.as_view(), name='test_image_update'),
    # files
    path('file/create/<int:test_id>/', views.TestFileCreate.as_view(), name='test_file_create'),
    path('file/delete/<int:pk>/', views.TestFileDelete.as_view(), name='test_file_delete'),
    path('file/update/<int:pk>/', views.TestFileUpdate.as_view(), name='test_file_update'),
    # checklists
    path('checklist/create/<int:test_id>/', views.TestChecklistCreate.as_view(), name='test_checklist_create'),
    path('checklist/delete/<int:pk>/', views.TestChecklistDelete.as_view(), name='test_checklist_delete'),
    path('checklist/update/<int:pk>/', views.TestChecklistUpdate.as_view(), name='test_checklist_update'),
    # checklist items
    path('checklist_item/create/<int:checklist_id>/', views.TestChecklistItemCreate.as_view(),
         name='test_checklist_item_create'),
    path('checklist_item/delete/<int:pk>/', views.TestChecklistItemDelete.as_view(),
         name='test_checklist_item_delete'),
    path('checklist_item/update/<int:pk>/', views.TestChecklistItemUpdate.as_view(),
         name='test_checklist_item_update'),
    # integer values
    path('int_value/create/<int:test_id>/', views.TestIntegerValueCreate.as_view(), name='test_int_value_create'),
    path('int_value/delete/<int:pk>/', views.TestIntegerValueDelete.as_view(), name='test_int_value_delete'),
    path('int_value/update/<int:pk>/', views.TestIntegerValueUpdate.as_view(), name='test_int_value_update'),

    # links
    path('test_link/create/<int:test_id>/', views.TestLinkCreate.as_view(), name='test_link_create'),
    path('test_link/delete/<int:pk>/', views.TestLinkDelete.as_view(), name='test_link_delete'),
    path('test_link/update/<int:pk>/', views.TestLinkUpdate.as_view(), name='test_link_update'),
    # comments
    path('test_comment/create/<int:test_id>/', views.TestCommentCreate.as_view(), name='test_comment_create'),
    path('test_comment/delete/<int:pk>/', views.TestCommentDelete.as_view(), name='test_comment_delete'),
    path('test_comment/update/<int:pk>/', views.TestCommentUpdate.as_view(), name='test_comment_update'),
]
