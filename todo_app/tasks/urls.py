from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.list_tasks),
    path('tasks/create/', views.create_task),
    path('tasks/<int:pk>/', views.update_task),
    path('tasks/<int:pk>/delete/', views.delete_task),
    path('tasks/reorder/', views.reorder_task),
]