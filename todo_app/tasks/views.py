# Create your views here.
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer

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
@api_view(['GET'])
def list_tasks(request):
    tasks = Task.objects.order_by('position')
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


# CREATE
@api_view(['POST'])
def create_task(request):
    last = Task.objects.order_by('-position').first()
    position = last.position + 1000 if last else 1000

    task = Task.objects.create(
        title=request.data.get('title'),
        description=request.data.get('description', ''),
        position=position
    )

    return Response(TaskSerializer(task).data)


# UPDATE
@api_view(['PUT'])
def update_task(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)

    task.title = request.data.get('title', task.title)
    task.description = request.data.get('description', task.description)
    task.save()

    return Response(TaskSerializer(task).data)


# DELETE
@api_view(['DELETE'])
def delete_task(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)

    task.delete()
    return Response({'success': True})


# REORDER 
@api_view(['POST'])
def reorder_task(request):
    task_id = request.data.get('id')
    new_index = request.data.get('newIndex')

    tasks = list(Task.objects.order_by('position'))
    
    try:
        # Find the task to move
        task = None
        for t in tasks:
            if t.id == task_id:
                task = t
                break

    except StopIteration:
        return Response({'error': 'Not found'}, status=404)

    tasks.remove(task)
    tasks.insert(new_index, task)

    prev = tasks[new_index - 1].position if new_index > 0 else None
    next_pos = tasks[new_index + 1].position if new_index < len(tasks) - 1 else None

    task.position = get_new_position(prev, next_pos)
    task.save()

    return Response(TaskSerializer(task).data)