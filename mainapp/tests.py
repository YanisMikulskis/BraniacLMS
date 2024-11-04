import time
from http import HTTPStatus

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.safari.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys

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
from django.contrib.auth import get_user_model

class TestMainPage(TestCase): #тест стартовой страницы

    def test_page_open(self):
        path = reverse('mainapp_namespace:main_page')# Create your tests here.
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)
        print(f'all ok')
class TestNewsPage(TestCase): #тесты для страницы новостей
    fixtures = {
        'authapp/fixtures/001_user_admin.json',
        'mainapp/fixtures/001_news_fixt.json'
    }

    def setUp(self): #логин воображаемого пользователя
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

    def test_page_open(self): #открытие страницы новостей
        path = reverse('mainapp_namespace:news_list')
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_page_open_detail(self): #открытие деталей новостей
        news_obj = News.objects.first()
        path = reverse('mainapp_namespace:news_detail', args=[news_obj.pk])
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)


    def test_page_open_create_deny_access(self): #защита от создания новостей неавт пользователями
        path = reverse('mainapp_namespace:news_create')
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_page_open_create_by_admin(self): # открытие страницы создания новостей модераторами
        path = reverse('mainapp_namespace:news_create')
        result = self.client_with_auth.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)


    def test_create_in_web(self): # создания новостей (модератором)
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




    def test_page_open_update_deny_access(self):#защита от изменения новостей неавт пользователями
        news_obj = News.objects.first()
        path = reverse('mainapp_namespace:news_update', args=[news_obj.pk])
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_page_open_update_by_admin(self):# открытие страницы изменения новостей модераторами
        news_obj = News.objects.first()
        path = reverse('mainapp_namespace:news_update', args=[news_obj.pk])
        result = self.client_with_auth.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_update_in_web(self): # изменение новостей (модератором)
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

    def test_delete_deny_access(self): #защита от удаления новостей неавт пользователями
        news_obj = News.objects.first()
        path = reverse('mainapp_namespace:news_delete', args=[news_obj.pk])
        result = self.client.post(path)
        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_delete_in_web(self): #удаление новости модератором
        news_obj = News.objects.first()
        path = reverse('mainapp_namespace:news_delete', args=[news_obj.pk])
        response = self.client_with_auth.post(path)
        news_obj.refresh_from_db()
        self.assertTrue(news_obj.deleted)


def is_redis_available(): # проверка включен редис или нет
    try:
        client = redis.StrictRedis(host='localhost', port=6379, db=0)
        client.ping()
        return True
    except redis.ConnectionError:
        return False
class TestCoursesWithMock(TestCase): # консервация объектов
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

class TestCoursesPage(TestCase): # открытие страницы курсов

    fixtures = {
        'mainapp/fixtures/002_course_fixt.json',
        'authapp/fixtures/001_user_admin.json'
    }

    def setUp(self):
        super().setUp()

        self.client_with_auth = Client()

        path_auth = reverse('authapp_namespace:login')
        self.client_with_auth.post(path_auth, data={'username': 'admin',
                                                    'password': 'admin'})
    def test_page_open_courses_list(self): #открытие странциы курсов
        path = reverse('mainapp_namespace:courses_page')
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_open_detail_course(self): #открытие деталей курсов
        all_courses = Courses.objects.all()
        for course in all_courses:
            path = reverse('mainapp_namespace:courses_details', args=[course.pk])
            result = self.client.get(path)
            self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_pay_course(self):
        course = Courses.objects.first()
        path = reverse('mainapp_namespace:courses_details', args=[course.pk])
        result = self.client.get(path)
        # self.assertContains(result, 'href="#" role="button"', html=True)
        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_pay_new_course_auth_user(self): #покупка нового курса
        course = Courses.objects.first()
        self.assertIsNotNone(course, 'Course should exist') # проверка существования
        path = reverse('authapp_namespace:add_course', args=[course.pk])
        user = get_user_model().objects.get(username='admin')
        counter_before = user.purchased_courses.count()

        self.client_with_auth.get(path) # подходит и для get_user_model
        print(f'alree {user.purchased_courses.count()}')
        counter_after = user.purchased_courses.count()
        self.assertGreater(counter_after, counter_before)

    def test_pay_already_user_course(self): #покупка существующего курса
        course = Courses.objects.first()
        self.assertIsNotNone(course, 'не существует курса')

        user = get_user_model().objects.get(username='admin')
        user.purchased_courses.add(course) #добавляем в ручную курс
        counter_before = user.purchased_courses.count()

        path = reverse('authapp_namespace:add_course', args=[course.pk]) #url добавления курса
        self.client_with_auth.get(path)# переходим

        counter_after = user.purchased_courses.count()
        self.assertEqual(counter_after, counter_before) # количество курсов в созданного юзера не должно измениться
class TestUserDate(TestCase):
    fixtures = {
        'authapp/fixtures/001_user_admin.json'
    }
    def setUp(self):
        super().setUp()
        self.client_with_auth = Client()
        path_auth = reverse('authapp_namespace:login')
        self.client_with_auth.post(path_auth, data={'username': 'admin',
                                                    'password': 'admin'})
    def test_page_open_edit_profile(self): # редактирование учетной записи
        user = get_user_model().objects.get(username='admin')
        path = reverse('authapp_namespace:profile_edit', args=[user.pk])
        result = self.client_with_auth.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)
    def test_page_open_my_course(self): # просмотр купленных курсов
        path = reverse('authapp_namespace:view_courses')
        result = self.client_with_auth.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_page_open_admin_panel(self): # открытие админ панели
        path = reverse('admin:index')
        result = self.client_with_auth.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)

class TestCRUDSelenium(StaticLiveServerTestCase):
    fixtures = {
        'authapp/fixtures/001_user_admin.json'
    }

    def setUp(self):
        super().setUp()
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(10)
        # self.test_login_by_selenium()

    def test_login_by_selenium(self):
        path_auth = reverse('authapp_namespace:login')
        login_url = f'{self.live_server_url}{path_auth}'
        self.selenium.get(login_url)

        username_input = self.selenium.find_element(By.NAME, 'username')
        password_input = self.selenium.find_element(By.NAME, 'password')

        username_input.send_keys('admin')
        password_input.send_keys('admin')
        password_input.send_keys(Keys.ENTER)
        main_page = reverse('mainapp_namespace:main_page')
        url_after_login = f'{self.live_server_url}{main_page}'
        # Ожидание, пока текущий URL не станет тем, что мы ожидаем
        WebDriverWait(self.selenium, 10).until(EC.url_to_be(url_after_login))

        self.current_url = self.selenium.current_url
        self.assertEqual(self.current_url, url_after_login)

    def test_CRUD_create(self):
        self.test_login_by_selenium() #логинимся, используя предыдущий тест

        news_button = self.selenium.find_element(By.LINK_TEXT, 'Новости') # находим текст-ссылку с надписью Новости
        news_button.click() # нажимаем

        path_news = f'{self.live_server_url}{reverse("mainapp_namespace:news_list")}' # текущий url после нажатия
        current_url = self.selenium.current_url # url на который перешел Selenium
        #self.assertEqual(current_url, path_news) # Сравниваем. Они должны быть идентичны


    def tearDown(self):

        # Close browser
        if self.selenium:
            self.selenium.quit()
        super().tearDown()


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




# class TestNewsSelenium(StaticLiveServerTestCase):
#     fixtures = {
#         "authapp/fixtures/001_user_admin.json",
#         "mainapp/fixtures/001_news_fixt.json"
#     }
#     def setUp(self):
#         super().setUp()
#         self.selenium = WebDriver()
#         self.selenium.implicitly_wait(10)
#         #Login
#
#         self.selenium.get(f"{self.live_server_url}{reverse('authapp_namespace:login')}")
#         button_enter = WebDriverWait(self.selenium, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR,
#                                                                                                '[type="submit"]')))
#         # button_enter = WebDriverWait(self.selenium, 5).until(EC.visbility_of_element_located(
#         #     (By.CSS_SELECTOR, '[type="submit"]')
#         # ))
#
#         self.selenium.find_element(By.ID, 'id_username').send_keys('admin')
#         self.selenium.find_element(By.ID, 'id_password').send_keys('admin')
#
#         button_enter.click()
#
#         #wait for footer
#         # footer = WebDriverWait(self.selenium, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'carousel-item')))
#         # self.selenium.get(f"{self.live_server_url}{reverse('mainapp_namespace:main_page')}")
#         # WebDriverWait(self.selenium, 5).until(EC.visibility_of_element_located(
#         #     (By.CLASS_NAME, 'list-unstyled'))
#         # )
#         # print(footer)
#     def test_create_button_clickable(self):
#         path_list = f"{self.live_server_url}{reverse('mainapp_namespace:news_list')}"
#         path_create = reverse("mainapp_namespace:news_create")
#         self.selenium.get(path_list)
#         print(f'start frame')
#         button_create = WebDriverWait(self.selenium, 10).until(
#             EC.visibility_of_element_located(
#                 (By.CSS_SELECTOR, f'[href="{path_create}"]'))
#         )
#         print("Trying to click button ...")
#         button_create.click()  # Test that button clickable
#         WebDriverWait(self.selenium, 10).until(EC.visibility_of_element_located((By.ID, "id_title")))
#         print("Button clickable!")
#         # With no element - test will be failed
#         # WebDriverWait(self.selenium, 5).until(
#         #     EC.visibility_of_element_located((By.ID, "id_title111"))
#         # )
#
#     def test_pick_color(self):
#         path = f"{self.live_server_url}{reverse('mainapp_namespace:main_page')}"
#         self.selenium.get(path)
#         navbar_el = WebDriverWait(self.selenium, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, "navbar")))
#         try:
#             self.assertEqual(
#                 navbar_el.value_of_css_property("background-color"),
#                 "rgb(255, 255, 155)",
#             )
#         except AssertionError:
#             with open("var/screenshots/001_navbar_el_scrnsht.png", "wb") as outf:
#                 outf.write(navbar_el.screenshot_as_png)
#             raise
#
#     def tearDown(self):
#         # Close browser
#         if self.selenium:
#             self.selenium.quit()
#         super().tearDown()