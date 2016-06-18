from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class TodoList(models.Model):
    # TODO: add user as a foreign key to the user table?
    # TODO: add a 'tag' field to allow users to tag and filter lists
    owner = models.ForeignKey(User, editable=False, default=None)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Todo(models.Model):
    parent_list = models.ForeignKey(TodoList, on_delete=models.CASCADE)
    item_text = models.CharField(max_length=200)
    completed = models.BooleanField()

    def __str__(self):
        return "%s--%s" % (self.item_text, self.completed)
