from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post

User = get_user_model()


class PostCreateFormTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_form_user')
        cls.group = Group.objects.create(
            title = 'тестовая группа для форм',
            slug = 'actors'
        )
        cls.post = Post.objects.create(
            text = 'Текстовый заголовок',
            author = cls.user,
        )

    def setUp(self) -> None:
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post_in_db(self):
        """Валидная форма создает запись в бд"""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'тестовый текст',
            'group': {self.group.id}
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            'posts:profile', 
            kwargs={'username': self.user}
            ))
        self.assertEqual(Post.objects.count(), posts_count+1)

    def test_author_can_edit_post(self):
        """Валидная форма изменяет запись в бд"""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Новый текст'
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            'posts:post_detail', 
            kwargs={'post_id': self.post.id}
            ))
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertTrue(Post.objects.filter(text='Новый текст').exists())
        self.assertEqual(response.status_code, HTTPStatus.OK)
        