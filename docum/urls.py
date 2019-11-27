from django.urls import path
from . import views

urlpatterns = [
    path('type/', views.TypeListView.as_view(), name='docum_types'),
    path('type/create/', views.TypeCreate.as_view(), name='docum_type_create'),
    path('type/<int:pk>/', views.TypeUpdate.as_view(), name='docum_type_update'),
    path('type/<int:pk>/delete/', views.TypeDelete.as_view(), name='docum_type_delete'),

    path('', views.DocumListView.as_view(), name='docums'),
    path('create/', views.DocumCreate.as_view(), name='docum_create'),
    path('<int:pk>/', views.DocumUpdate.as_view(), name='docum_update'),
    path('<int:pk>/delete/', views.DocumDelete.as_view(), name='docum_delete'),
]
