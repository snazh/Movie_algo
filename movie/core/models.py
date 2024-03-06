from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.


class UserMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="user")
    movieID = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.user.username}-{self.movieID}'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user')
    movieID = models.IntegerField()
    content = models.TextField(blank=False)
    created_time = models.DateTimeField( verbose_name="create time", default=timezone.now)

    def __str__(self):
        return f'{self.user.username}-{self.movieID}'
