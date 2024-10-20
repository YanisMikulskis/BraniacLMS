from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class TestMainPage(TestCase):
    def test_page_open(self):
        path = reverse('mainapp_namespace:main_page')# Create your tests here.
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)

class TestNewsPage(TestCase):
    def test_page_open(self):
        path = reverse('mainapp_namespace:news_list')
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)