from django.db import models
from src.account.models import TgUser


class Task(models.Model):
    title = models.CharField(max_length=200)
    is_done = models.BooleanField(default=False)

    owner = models.ForeignKey(TgUser, related_name='tasks', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
