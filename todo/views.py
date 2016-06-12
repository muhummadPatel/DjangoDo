from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views.decorators.http import require_GET

from .models import Todo, TodoList


@require_GET
def index(request):
    return render(request, 'todo/index.html', {})


@require_GET
def lists(request):
    todo_lists = get_list_or_404(TodoList)
    context = {
        'todo_lists': todo_lists
    }
    return render(request, 'todo/lists.html', context)


@require_GET
def lists_detail(request, list_id):
    todo_list = get_object_or_404(TodoList, pk=list_id)
    todos = get_list_or_404(Todo, parent_list=list_id)

    context = {
        'todo_list': todo_list,
        'todos': todos
    }

    return render(request, 'todo/lists_detail.html', context)
