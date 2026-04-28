from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.tasks),                 # GET, POST
    path('tasks/<int:pk>/', views.task_detail),  # GET, PUT, DELETE
    path('tasks/reorder/', views.reorder_task),  # POST
]