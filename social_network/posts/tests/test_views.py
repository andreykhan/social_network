from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django import forms

from posts.models import Post, Group

User = get_user_model()


class PostPagesTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_author')
        cls.post = Post.objects.create(
            text = 'Текстовый заголовок',
            author = cls.user,
        )
        cls.group = Group.objects.create(
            title = 'тестовая группа',
            slug = 'singers'
        )
        cls.templates_and_urls = {
            'posts/index.html': reverse('posts:main_page'),
            'posts/group_list.html': (
                reverse('posts:group', kwargs={'slug': cls.group.slug})
            ),
            'posts/profile.html': (
                reverse('posts:profile', kwargs={'username': cls.user})
            ),
            'posts/post_detail.html': (
                reverse('posts:post_detail', kwargs={'post_id': cls.post.id})
            ),
            'posts/create_post.html': reverse('posts:post_create'),
            'posts/edit_post.html': (
                reverse('posts:post_edit', kwargs={'post_id': cls.post.id})
            ),
        }

    def setUp(self) -> None:
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_users_correct_templates(self):
        """страницы используют соответствующие шаблоны"""
        for template, reverse_name in self.templates_and_urls.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_home_page_show_correct_context(self):
        """Шаблон главной страницы сформирован с правильным контекстом"""
        response = self.authorized_client.get(reverse('posts:main_page'))
        first_object = response.context["page_obj"][0]
        post_text_0 = first_object.text
        post_author_0 = first_object.author
        self.assertEqual(post_text_0, 'Текстовый заголовок')
        self.assertEqual(post_author_0, PostPagesTest.user)

    def  test_group_pages_show_correct_context(self):
        """Шаблон группы сформирован с правильным контекстом"""
        response = self.authorized_client.get(
            reverse('posts:group', kwargs={'slug': self.group.slug})
            )
        first_object = response.context["group"]
        group_title_0 = first_object.title
        group_slug_0 = first_object.slug
        self.assertEqual(group_title_0, 'тестовая группа')
        self.assertEqual(group_slug_0, 'singers')


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_paginator')
        cls.group = Group.objects.create(
            title = 'тестовая группа',
            slug = 'singers'
        )
        cls.posts = []
        for i in range(13):
            cls.posts.append(Post(
                text=f'Тестовый пост {i}',
                author=cls.user,
                group=cls.group
            )
            )
        Post.objects.bulk_create(cls.posts)
        cls.pages_and_posts_count = {
            reverse('posts:main_page'): 10,
            reverse('posts:group', kwargs={'slug': cls.group.slug}): 6,
            reverse('posts:profile', kwargs={'username': cls.user}): 6
        }
    def setUp(self) -> None:
        self.guest_client = Client()

    def test_first_page_contains_n_records(self):
        """проверка паджинатора 1й страницы"""
        for pages, posts_count in self.pages_and_posts_count.items():
            with self.subTest(pages=pages):
                response = self.guest_client.get(pages)
                self.assertEqual(len(response.context['page_obj']), posts_count)
