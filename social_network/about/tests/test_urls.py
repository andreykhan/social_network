from django.test import TestCase, Client
from http import HTTPStatus

class AboutUrlTests(TestCase):
    def setUp(self) -> None:
        self.guest_client = Client()

    def test_urls_exists_at_desired_location(self):
        """страницы "author/", "tech/" доступны"""
        urls = ["/about/author/", "/about/tech/"]
        for i in urls:
            with self.subTest(i):
                response = self.guest_client.get(i)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_users_correct_templates(self):
        urls_and_templates = {
            "/about/author/": "about/about_author.html",
            "/about/tech/": "about/about_tech.html"
        }
        for url, template in urls_and_templates.items():
            with self.subTest(url):
                response = self.guest_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_incorrect_url_returns_404(self):
        """запрос к несуществующей странице возвращает 404"""
        response = self.guest_client.get('/about/money/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
    
    