from django.db import models
from django.contrib.auth.models import User

class TodoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)
    title = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Task(models.Model):
    todo_list = models.ForeignKey(TodoList, on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=255)
    description = models.TextField(default='', null=True, blank=True, max_length=80)
    completed = models.BooleanField(default=False)
    priority = models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')], default=2)
    due = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
