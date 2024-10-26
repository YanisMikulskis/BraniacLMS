from http import HTTPStatus

import selenium

import redis
from unittest import mock, skipUnless
from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail as django_mail
import authapp.models
import mainapp.tasks
from .models import News, Courses
import pickle

class TestMainPage(TestCase):

    def test_page_open(self):
        path = reverse('mainapp_namespace:main_page')# Create your tests here.
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)
        print(f'all ok')
class TestNewsPage(TestCase):
    fixtures = {
        'authapp/fixtures/001_user_admin.json',
        'mainapp/fixtures/001_news_fixt.json'
    }

    def setUp(self):
        super().setUp()
        self.client_with_auth = Client()
        path_auth = reverse('authapp_namespace:login')
        self.client_with_auth.post(path_auth, data={'username': 'admin',
                                                    'password': 'admin'})

    def test_page_open(self):
        path = reverse('mainapp_namespace:news_list')
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_page_open_detail(self):
        news_obj = News.objects.first()
        path = reverse('mainapp_namespace:news_detail', args=[news_obj.pk])
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)


    def test_page_open_create_deny_access(self):
        path = reverse('mainapp_namespace:news_create')
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_page_open_create_by_admin(self):
        path = reverse('mainapp_namespace:news_create')
        result = self.client_with_auth.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_create_in_web(self):
        counter_before = News.objects.count()
        path = reverse('mainapp_namespace:news_create')
        self.client_with_auth.post(
            path,
            data = {
                'title': 'NewTestNews001',
                'preambule': 'NewTestNews001',
                'body': 'NewTestNews001'
            }
        )
        self.assertGreater(News.objects.count(), counter_before)

    def test_page_open_update_deny_access(self):
        news_obj = News.objects.first()
        path = reverse('mainapp_namespace:news_update', args=[news_obj.pk])
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_page_open_update_by_admin(self):
        news_obj = News.objects.first()
        path = reverse('mainapp_namespace:news_update', args=[news_obj.pk])
        result = self.client_with_auth.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_update_in_web(self):
        new_title = 'NewsTestTitle0001'
        news_obj = News.objects.first()
        self.assertNotEqual(news_obj.title, new_title)
        path = reverse('mainapp_namespace:news_update', args=[news_obj.pk])
        result = self.client_with_auth.post(
            path,
            data = {
                'title': new_title,
                'preambule': news_obj.preambule,
                'body': news_obj.body
            }
        )
        self.assertEqual(result.status_code, HTTPStatus.FOUND)
        news_obj.refresh_from_db()
        self.assertEqual(news_obj.title, new_title)

    def test_delete_deny_access(self):
        news_obj = News.objects.first()
        path = reverse('mainapp_namespace:news_delete', args=[news_obj.pk])
        result = self.client.post(path)
        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_delete_in_web(self):
        news_obj = News.objects.first()
        path = reverse('mainapp_namespace:news_delete', args=[news_obj.pk])
        response = self.client_with_auth.post(path)
        news_obj.refresh_from_db()
        self.assertTrue(news_obj.deleted)


def is_redis_available():
    try:
        client = redis.StrictRedis(host='localhost', port=6379, db=0)
        client.ping()
        return True
    except redis.ConnectionError:
        return False
class TestCoursesWithMock(TestCase):
    fixtures = {
        "authapp/fixtures/001_user_admin.json",
        "mainapp/fixtures/002_course_fixt.json",
        "mainapp/fixtures/003_lesson_fixt.json",
        "mainapp/fixtures/004_courseteachers_fixt.json"
    }
    @skipUnless(is_redis_available(), 'Redis is not available')
    def test_page_open_detail(self): #для успешного выполнения теста надо включить редис!
        course_obj = Courses.objects.first()
        print(course_obj)
        path = reverse('mainapp_namespace:courses_details', args=[course_obj.pk])
        with open('mainapp/fixtures/006_feedback_list_9.bin', 'rb') as inpf,\
            mock.patch('django.core.cache.cache.get') as mocked_cache:
            mocked_cache.return_value = pickle.load(inpf)
            print(mocked_cache.called)
            result = self.client.get(path)
            self.assertEqual(result.status_code, HTTPStatus.OK)
            self.assertTrue(mocked_cache.called)


class TestTaskMailSend(TestCase):
    fixtures = {"authapp/fixtures/001_user_admin.json"}
    def test_mail_send(self):
        message_text = 'test_message_text'
        user_obj = authapp.models.CustomUser.objects.first()
        mainapp.tasks.send_feedback_mail(
            {'user_id': user_obj.id,
             'message': message_text}
        )
        self.assertEqual(django_mail.outbox[0].body, message_text)


class TestNewsSelenium(TestCase):
    fixtures = {
        "authapp/fixtures/001_user_admin.json",
        "mainapp/fixtures/001_news_fixt.json"
    }

    def setUp(self):
        super().setUp()
        self.selenium = WebDriver(exe)