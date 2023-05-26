from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse


class AboutViewsTest(TestCase):
    def setUp(self) -> None:
        self.guest_client = Client()

    def test_about_page_accessible_by_name(self):
        """
        URL, генерируемый при помощи имен about:author 
        и about:tech, доступен.
        """
        urls_and_names = ['about:author', 'about:tech']
        for url in urls_and_names:
            with self.subTest(url = url):
                response = self.guest_client.get(reverse(url))
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_about_page_uses_correct_template(self):
        """
        При запросам к about:author 
        и about:tech применяется корректные шаблоны
        """
        pages_and_templates = {
            'about:author': 'about/about_author.html',
            'about:tech': 'about/about_tech.html'
        }
        for page, template in pages_and_templates.items():
            with self.subTest(page=page):
                response = self.guest_client.get(reverse(page))
                self.assertTemplateUsed(response, template)
