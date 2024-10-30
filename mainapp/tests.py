from http import HTTPStatus

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.safari.webdriver import WebDriver
from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
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
        # self.selenium = WebDriver()
        # self.selenium.implicitly_wait(10)
        # self.selenium

        # self.selenium = WebDriver()
        # self.selenium.implicitly_wait(10)
        # # Login
        # self.selenium.get(f"{self.live_server_url}{reverse('authapp_namespace:login')}")
        # button_enter = WebDriverWait(self.selenium, 5).until(EC.visibility_of_element_located([By.CSS_SELECTOR,
        #                                                                                        '[type="submit"]']))

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


class TestNewsSelenium(StaticLiveServerTestCase):
    fixtures = {
        "authapp/fixtures/001_user_admin.json",
        "mainapp/fixtures/001_news_fixt.json"
    }

    def setUp(self):
        super().setUp()
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(10)
        #Login

        self.selenium.get(f"{self.live_server_url}{reverse('authapp_namespace:login')}")
        button_enter = WebDriverWait(self.selenium, 5).until(EC.visibility_of_element_located([By.CSS_SELECTOR,
                                                                                               '[type="submit"]']))
        # button_enter = WebDriverWait(self.selenium, 5).until(EC.visbility_of_element_located(
        #     (By.CSS_SELECTOR, '[type="submit"]')
        # ))

        self.selenium.find_element(By.ID, 'id_username').send_keys('admin')
        self.selenium.find_element(By.ID, 'id_password').send_keys('admin')
        button_enter.click()
        #wait for footer
        WebDriverWait(self.selenium, 20).until(EC.visibility_of_element_located(
            (By.CLASS_NAME, 'list-unstyled'))
        )

    def test_create_button_clickable(self):
        path_list = f"{self.live_server_url}{reverse('mainapp_namespace:news_list')}"
        path_add = reverse("mainapp_namespace:news_create")
        self.selenium.get(path_list)
        print(f'start frame')
        button_create = WebDriverWait(self.selenium, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, f'[href="{path_add}"]'))
        )
        print("Trying to click button ...")
        button_create.click()  # Test that button clickable
        WebDriverWait(self.selenium, 10).until(EC.visibility_of_element_located((By.ID, "id_title")))
        print("Button clickable!")
        # With no element - test will be failed
        # WebDriverWait(self.selenium, 5).until(
        #     EC.visibility_of_element_located((By.ID, "id_title111"))
        # )

    def test_pick_color(self):
        path = f"{self.live_server_url}{reverse('mainapp_namespace:main_page')}"
        self.selenium.get(path)
        navbar_el = WebDriverWait(self.selenium, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, "navbar")))
        try:
            self.assertEqual(
                navbar_el.value_of_css_property("background-color"),
                "rgb(255, 255, 155)",
            )
        except AssertionError:
            with open("var/screenshots/001_navbar_el_scrnsht.png", "wb") as outf:
                outf.write(navbar_el.screenshot_as_png)
            raise

    def tearDown(self):
        # Close browser
        if self.selenium:
            self.selenium.quit()
        super().tearDown()