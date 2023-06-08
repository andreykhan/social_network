from django.contrib.auth import get_user_model
from django.db import models

from core.models import CreateModel

User = get_user_model()


class Group(models.Model):
    title = models.TextField()
    slug = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(
        'Текст поста',
        help_text='Введите текст поста'
    )
    pub_date = models.DateTimeField(
        'дата публикации',
        auto_now_add=True,
        null=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='posts',
        verbose_name='Автор'
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Группа',
        help_text='Группа, к которой будет относиться пост'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True
    )

    def __str__(self):
        return self.text[:15]
    

class Comment(CreateModel):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='comments'
    )
    text = models.TextField()


class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )
