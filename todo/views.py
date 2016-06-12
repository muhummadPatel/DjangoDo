from django.shortcuts import get_list_or_404, render

from .models import Todo, TodoList


def index(request):
    return render(request, 'todo/index.html', {})


def lists(request):
    selected_lists = get_list_or_404(TodoList)
    context = {
        "list_names": [l.name for l in selected_lists]
    }
    return render(request, 'todo/lists.html', context)
