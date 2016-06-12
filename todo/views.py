from django.shortcuts import render


def index(request):
    return render(request, 'todo/index.html', {})


def lists(request):
    return render(request, 'todo/lists.html', {})
