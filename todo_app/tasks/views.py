# Create your views here.
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404

import logging

logger = logging.getLogger(__name__)

# Utility function
def get_new_position(prev, next):
    if prev is None and next is None:
        return 1000
    if prev is None:
        return next - 1000
    if next is None:
        return prev + 1000
    return (prev + next) / 2


# LIST
@api_view(['GET', 'POST'])
def tasks(request):
    if request.method == 'GET':
        tasks = Task.objects.order_by('position')
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        title = request.data.get('title')

        if not title:
            return Response(
                {"error": "Title is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        last = Task.objects.order_by('-position').first()
        position = last.position + 1000 if last else 1000

        task = Task.objects.create(
            title=title,
            description=request.data.get('description', ''),
            position=position
        )

        return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
    
@api_view(['PUT', 'DELETE'])
def task_detail(request, pk):
    if request.method == 'PUT':
        task = get_object_or_404(Task, pk=pk)

        title = request.data.get('title')
        description = request.data.get('description')

        if title is not None and not isinstance(title, str):
            return Response(
                {"error": "Title must be a string."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if description is not None and not isinstance(description, str):
            return Response(
                {"error": "Description must be a string."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # update safely
        if title is not None:
            task.title = title

        if description is not None:
            task.description = description

        task.save()

        return Response(TaskSerializer(task).data, status=status.HTTP_200_OK)
    
    if request.method == 'DELETE':
        task = get_object_or_404(Task, pk=pk)

        task.delete()

        return Response(
            {"message": f"Task {pk} deleted successfully."},
            status=status.HTTP_200_OK
        )

# REORDER 
@api_view(['POST'])
def reorder_task(request):
    task_id = request.data.get('id')
    new_index = request.data.get('newIndex')

    if task_id is None or new_index is None:
        return Response(
            {"error": "Both 'id' and 'newIndex' are required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        new_index = int(new_index)
    except (TypeError, ValueError):
        return Response(
            {"error": "'newIndex' must be an integer."},
            status=status.HTTP_400_BAD_REQUEST
        )

    tasks = list(Task.objects.order_by('position'))

    task = next((t for t in tasks if t.id == task_id), None)
    if not task:
        return Response(
            {"error": f"Task with id {task_id} not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    if new_index < 0 or new_index >= len(tasks):
        return Response(
            {"error": f"'newIndex' must be between 0 and {len(tasks) - 1}."},
            status=status.HTTP_400_BAD_REQUEST
        )

    tasks.remove(task)
    tasks.insert(new_index, task)

    prev_pos = tasks[new_index - 1].position if new_index > 0 else None
    next_pos = tasks[new_index + 1].position if new_index < len(tasks) - 1 else None

    task.position = get_new_position(prev_pos, next_pos)
    task.save()

    return Response(TaskSerializer(task).data, status=status.HTTP_200_OK)