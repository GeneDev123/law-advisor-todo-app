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

# Utility function (gap-based ordering)
def get_new_position(prev, next):
    if prev is None and next is None:
        return 1000000
    if prev is None:
        return next - 1000000
    if next is None:
        return prev + 1000000

    return (prev + next) / 2


# LIST + CREATE
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

        last = Task.objects.order_by('-position').only('position').first()
        position = last.position + 1000000 if last else 1000000

        task = Task.objects.create(
            title=title,
            description=request.data.get('description', ''),
            position=position
        )

        return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)

# UPDATE + DELETE
@api_view(['PUT', 'DELETE'])
def task_detail(request, pk):

    task = get_object_or_404(Task, pk=pk)

    if request.method == 'PUT':

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

        if title is not None:
            task.title = title

        if description is not None:
            task.description = description

        task.save()

        return Response(TaskSerializer(task).data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        task.delete()

        return Response(
            {"message": f"Task {pk} deleted successfully."},
            status=status.HTTP_200_OK
        )


# REORDER (OPTIMIZED FOR 1M ROWS)
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
        task_id = int(task_id)
        new_index = int(new_index)
    except (TypeError, ValueError):
        return Response(
            {"error": "'id' and 'newIndex' must be integers."},
            status=status.HTTP_400_BAD_REQUEST
        )

    task = get_object_or_404(Task, id=task_id)

    # Get all tasks EXCEPT the one being moved (IMPORTANT OPTIMIZATION)
    qs = Task.objects.exclude(id=task_id).order_by('position')

    total = qs.count()

    if new_index < 0 or new_index > total:
        return Response(
            {"error": f"'newIndex' must be between 0 and {total}."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Fetch only neighbors (NO FULL LIST LOAD)
    prev_task = None
    next_task = None

    if new_index > 0:
        prev_task = qs[new_index - 1]

    if new_index < total:
        next_task = qs[new_index]

    prev_pos = prev_task.position if prev_task else None
    next_pos = next_task.position if next_task else None

    # Assign new fractional/gap position
    task.position = get_new_position(prev_pos, next_pos)
    task.save()

    return Response(TaskSerializer(task).data, status=status.HTTP_200_OK)