from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.timezone import datetime

class CustomUser(AbstractUser):
    pass

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')
    state = models.BooleanField(default=False)
    is_superuser_task = models.BooleanField(default=False)
    visible_to_all = models.BooleanField(default=False)
    visible_to = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='visible_tasks', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

class SuperuserTaskVisibility(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='visibilities')
    visible_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('task', 'visible_to')