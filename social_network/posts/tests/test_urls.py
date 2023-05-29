from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from posts.models import Group, Post

User = get_user_model()


class PostUrlTests(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_author')
        cls.post = Post.objects.create(
            text = 'Текстовый заголовок',
            pub_date = 'May 19, 2023, 10:32 a.m.',
            author = cls.user,
        )
        cls.group = Group.objects.create(
            title = 'тестовая группа',
            slug = 'actors'
        )
        cls.unauthorized_pages = [
            "/",
            "/group/actors/",
            "/profile/test_author/",
            f"/posts/{cls.post.id}/",
        ]
        cls.authorized_pages = [
            "/create/",
            f"/posts/{cls.post.id}/edit/",
        ]
        cls.templates_url_names = {
            "/": "posts/index.html",
            "/group/actors/": "posts/group_list.html",
            "/profile/test_author/": "posts/profile.html",
            f"/posts/{cls.post.id}/": "posts/post_detail.html",
            "/create/": "posts/create_post.html",
            f"/posts/{cls.post.id}/edit/": "posts/edit_post.html",
        }
        cls.redirect_pages = {
            "/create/": "/auth/login/?next=/create/",
            f"/posts/{cls.post.id}/edit/": f"/auth/login/?next=/posts/{cls.post.id}/edit/",
            f"/posts/{cls.post.id}/comment/": f"/auth/login/?next=/posts/{cls.post.id}/comment/"
        }

    def setUp(self) -> None:
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(PostUrlTests.user)

    def test_unauthorized_urls_exists_at_desired_location(self):
        """
        Страницы /,group/<slug:slug>/,profile/<slug:username>/,posts/<int:post_id>
        доступны любому пользователю.
        """
        for i in self.unauthorized_pages:
            with self.subTest(i=i):
                response = self.guest_client.get(i)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_authorized_urls_exists_at_desired_location(self):
        """
        Страницы /create, f"/posts/{post.id}/edit/",
        f"/posts/{post.id}/comment/"
        доступны авторизованным пользователям.
        """
        for i in self.authorized_pages:
            with self.subTest(i=i):
                response = self.authorized_client.get(i)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_redirects_anonymous(self):
        """
        Страницы "/create/",/posts/{post.id}/edit/,
        f"/posts/{post.id}/comment/"
        редиректят неавторизованных юзеров
        """
        for page, url in self.redirect_pages.items():
            with self.subTest(page=page):
                response = self.guest_client.get(page, follow=True)
                self.assertRedirects(response, url)

    def test_incorrect_page_does_not_exists(self):
        """Запрос к несуществующей странице возвращает ошибку 404"""
        response = self.guest_client.get('/kill/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        for address, template in self.templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)
