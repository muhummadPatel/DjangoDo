from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views.decorators.http import require_GET, require_POST, require_http_methods

from .models import Todo, TodoList


# TODO: POST a new list
# TODO: POST to update the items in a list

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
@require_http_methods(['GET', 'POST'])
def lists(request):
    if request.method == 'GET':
        user_todo_lists = TodoList.objects.filter(owner__exact=request.user).order_by('name')
        response_data = serializers.serialize('json', user_todo_lists)
        return HttpResponse(response_data, content_type='application/json')

    elif request.method == 'POST':
        try:
            new_list_name = request.POST['todolist_name']
            if new_list_name == '':
                raise ValueError('Cannot create list with empty name')

            new_list = TodoList(name=new_list_name, owner=request.user)
            new_list.save()
            return HttpResponse('', status=200)
        except AttributeError, ValueError:
            return HttpResponse('', status=400)


@login_required
@require_POST
def delete_list(request, list_id):
    # TODO: handle other errors? are there any other errors?
    todo_list = get_object_or_404(TodoList, pk=list_id, owner__exact=request.user)
    todo_list.delete()
    return HttpResponse('', status=200)


@login_required
@require_http_methods(['GET', 'POST'])
def lists_items(request, list_id):
    # do this first get so that a 404 is raised if the list does not exist
    todo_list = get_object_or_404(TodoList, pk=list_id, owner__exact=request.user)

    if request.method == 'GET':
        todo_items = []
        try:
            todo_items = Todo.objects.filter(parent_list=list_id).order_by('completed', 'item_text')
        except Todo.DoesNotExist:
            # if the list is currently empty, return an empty response to the client
            pass

        response_data = serializers.serialize('json', todo_items)
        return HttpResponse(response_data, content_type='application/json')

    elif request.method == 'POST':
        try:
            # NOTE: This sort of tedious manual error checking can be eliminated
            # for larger forms by using a form class (in forms.py) to handle
            # validating form submission inputs.
            new_item_text = request.POST['item_text']
            if new_item_text == '':
                raise ValueError('Cannot create item with empty item_text')

            new_item = Todo(parent_list=todo_list, item_text=new_item_text, completed=False)
            new_item.save()
            return HttpResponse('', status=200)
        except AttributeError, ValueError:
            return HttpResponse('', status=400)


@login_required
@require_POST
def edit_item(request, list_id, item_id):
    todo_list = get_object_or_404(TodoList, pk=list_id, owner__exact=request.user)
    todo_item = get_object_or_404(Todo, pk=item_id)

    status = (request.POST['item_status'] == 'true')
    todo_item.completed = status
    todo_item.save()
    return HttpResponse('', status=200)


@login_required
@require_POST
def delete_item(request, list_id, item_id):
    # TODO: handle other errors? are there any other errors?
    todo_list = get_object_or_404(TodoList, pk=list_id, owner__exact=request.user)
    todo_item = get_object_or_404(Todo, pk=item_id)
    todo_item.delete()
    return HttpResponse('', status=200)
