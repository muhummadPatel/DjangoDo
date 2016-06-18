from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views.decorators.http import require_GET, require_http_methods

from .models import Todo, TodoList


@require_GET
def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('todo:home'))
    else:
        return render(request, 'todo/index.html', {})


@login_required
def home(request):
    return render(request, 'todo/home.html', {})


@login_required
@require_GET
def lists(request):
    todo_lists = get_list_or_404(TodoList)
    context = {
        'todo_lists': todo_lists
    }
    return render(request, 'todo/lists.html', context)


@require_http_methods(['GET', 'POST'])
def lists_detail(request, list_id):
    if request.method == 'GET':
        todo_list = get_object_or_404(TodoList, pk=list_id)
        todos = get_list_or_404(Todo, parent_list=list_id)

        context = {
            'todo_list': todo_list,
            'todos': todos
        }

        return render(request, 'todo/lists_detail.html', context)

    elif request.method == 'POST':
        todo_list = get_object_or_404(TodoList, pk=list_id)
        todos = get_list_or_404(Todo, parent_list=list_id)

        completed_todos = [todo for todo in request.POST.keys()]
        for todo in todos:
            # TODO: Do this as a transaction. Possible race condition here? F()?
            updated_state = str(todo.id) in completed_todos
            if not todo.completed == updated_state:
                todo.completed = updated_state
                todo.save()

        context = {
            'todo_list': todo_list,
            'todos': todos,
            'message': "Successfully updated"
        }

        return render(request, 'todo/lists_detail.html', context)
