from django.test import TestCase, Client
from http import HTTPStatus

class UsersUrlTests(TestCase):
    def setUp(self) -> None:
        self.guest_client = Client()

    def test_urls_exists_at_desired_location(self):
        """
        страницы "/auth/logout/","/auth/login/","/auth/signup/",
        "/auth/passwordreset/" доступны всем пользователям
        """
        urls = [
            "/auth/logout/",
            "/auth/login/",
            "/auth/signup/",
            "/auth/passwordreset/"
        ]
        for i in urls:
            with self.subTest(i=i):
                response = self.guest_client.get(i)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_uses_correct_templates(self):
        urls_and_templates = {
            "/auth/logout/": "users/logged_out.html",
            "/auth/login/": "users/login.html",
            "/auth/signup/": "users/signup.html",
            "/auth/passwordreset/": "users/password_reset.html"
        }
        for url, template in urls_and_templates.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertTemplateUsed(response, template)
    
    def test_incorrect_url_return_404(self):
        response = self.guest_client.get("/auth/test")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
