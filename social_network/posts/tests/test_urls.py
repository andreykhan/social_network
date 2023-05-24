from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from posts.models import Post, Group

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

    def setUp(self) -> None:
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(PostUrlTests.user)

    def test_home_url_exists_at_desired_location(self):
        """Страница / доступна любому пользователю."""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_group_info_url_exists_at_desired_location(self):
        """Страница group/<slug:slug>/ доступна любому пользователю."""
        response = self.guest_client.get('/group/actors/')
        self.assertEqual(response.status_code, 200)

    def test_user_profile_url_exists_at_desired_location(self):
        """Страница profile/<slug:username>/ доступна любому пользователю."""
        response = self.guest_client.get('/profile/test_author/')
        self.assertEqual(response.status_code, 200)

    def test_post_detail_url_exists_at_desired_location(self):
        """Страница posts/<int:post_id> доступна любому пользователю."""
        response = self.guest_client.get(f"/posts/{self.post.id}/")
        self.assertEqual(response.status_code, 200)

    def test_post_create_url_exists_at_desired_location_authorized(self):
        """Страница create/ доступна авторизованному пользователю."""
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, 200)
    
    def test_post_edit_url_exists_at_desired_location_authorized(self):
        """Страница posts/<int:post_id>/edit/ доступна авторизованному пользователю."""
        response = self.authorized_client.get(f"/posts/{self.post.id}/edit/")
        self.assertEqual(response.status_code, 200)

    def test_post_create_url_redirect_anonymous(self):
        """Страница по адресу create/ перенаправит анонимного
        пользователя на страницу логина.
        """
        response = self.guest_client.get('/create/', follow=True)
        self.assertRedirects(
            response, '/auth/login/?next=/create/'
        )

    def test_post_edit_url_redirect_anonymous(self):
        """Страница по адресу posts/<int:post_id>/edit/перенаправит анонимного пользователя на страницу логина."""
        response = self.guest_client.get(f"/posts/{self.post.id}/edit/", follow=True)
        self.assertRedirects(
            response, f"/auth/login/?next=/posts/{self.post.id}/edit/"
        )

    def test_incorrect_page_does_not_exists(self):
        """Запрос к несуществующей странице возвращает ошибку 404"""
        response = self.guest_client.get('/kill/')
        self.assertEqual(response.status_code, 404)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            '/': 'posts/index.html',
            '/group/actors/': 'posts/group_list.html',
            '/profile/test_author/': 'posts/profile.html',
            f"/posts/{self.post.id}/": 'posts/post_detail.html',
            '/create/': 'posts/create_post.html',
            f"/posts/{self.post.id}/edit/": 'posts/edit_post.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)
