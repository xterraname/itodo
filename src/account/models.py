from django.db import models


class TgUser(models.Model):
    user_id = models.IntegerField(unique=True)

    username = models.CharField(max_length=200, null=True, blank=True)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)

    language_code = models.CharField(max_length=5, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.user_id)
