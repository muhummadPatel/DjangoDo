from __future__ import unicode_literals

from django.db import models


class TodoList(models.Model):
    # TODO: add user as a foreign key to the user table?
    # TODO: add a 'tag' field to allow users to tag and filter lists
    name = models.CharField(max_length=50)


class Todo(models.Model):
    parent_list = models.ForeignKey(TodoList, on_delete=models.CASCADE)
    item_text = models.CharField(max_length=200)
    completed = models.BooleanField()
