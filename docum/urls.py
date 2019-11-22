from django.urls import path
from . import views

urlpatterns = [
    path('type/', views.TypeListView.as_view(), name='types'),
    path('type/create/', views.TypeCreate.as_view(), name='type_create'),
    path('type/<int:pk>/', views.TypeUpdate.as_view(), name='type_update'),
    path('type/delete/<int:pk>/', views.TypeDelete.as_view(), name='type_delete'),
]
