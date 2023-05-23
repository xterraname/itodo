from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    is_done = models.BooleanField(default=False)

    owner = models.ForeignKey(User, related_name='tasks', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
