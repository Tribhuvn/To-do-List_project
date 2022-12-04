from django.db import models
from django.contrib.auth.models import User
from mysite.models import UserSession

# Create your models here.


class ToDoItems(models.Model):
    item_name = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    session = models.ForeignKey(UserSession, to_field='session_id', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.item_name


