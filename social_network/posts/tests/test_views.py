import shutil
import tempfile

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from posts.models import Group, Post

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


TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class ImagesTests(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_for_images')
        cls.group = Group.objects.create(
            title = 'wafmawfmwafmwa',
            slug = 'actors'
        )
        cls.small_gif = (
            b"\x47\x49\x46\x38\x39\x61\x02\x00"
            b"\x01\x00\x80\x00\x00\x00\x00\x00"
            b"\xFF\xFF\xFF\x21\xF9\x04\x00\x00"
            b"\x00\x00\x00\x2C\x00\x00\x00\x00"
            b"\x02\x00\x01\x00\x00\x02\x02\x0C"
            b"\x0A\x00\x3B"
        )
        cls.uploaded = SimpleUploadedFile(
            name="small.gif", content=cls.small_gif, content_type="image/gif"
        )
        cls.post = Post.objects.create(
            text = 'Тесты картинок',
            author = cls.user,
            image = cls.uploaded,
            group = cls.group
        )
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self) -> None:
        self.guest_client = Client()

    def test_image_in_all_pages(self):
        """
        картина передается на /,group/<slug:slug>/,
        profile/<slug:username>/
        """
        pages = [
            reverse('posts:main_page'),
            reverse('posts:group', kwargs={'slug': self.group.slug}),
            reverse('posts:profile', kwargs={'username': self.user}),
        ]
        for page in pages:
            with self.subTest(page=page):
                response = self.guest_client.get(page)
                self.assertEqual(response.context['page_obj'][0].image, self.post.image)

    def test_image_in_post_detail_page(self):
        """картинка передается на страницу post_detail"""
        response = self.guest_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.id})
        )
        obj = response.context['page_obj']
        self.assertEqual(obj.image, self.post.image)

    def test_image_in_page(self):
        """Проверяем что пост с картинкой создается в БД"""
        self.assertTrue(
            Post.objects.filter(text="Тесты картинок", image="posts/small.gif").exists()
        )
