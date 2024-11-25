import time
import pickle
import authapp.models
import mainapp.tasks
import redis
import emoji

import selenium.common.exceptions

from http import HTTPStatus
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.safari.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from unittest import mock, skipUnless, skip
from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail as django_mail
from .models import News, Courses
from django.contrib.auth import get_user_model
from screeninfo import get_monitors


class TestMainPage(TestCase):  # тест стартовой страницы
    """
    Тест стартовой страницы
    """
    def test_page_open(self):
        path = reverse('mainapp_namespace:main_page')  # путь к стартовой странице.
        result = self.client.get(path) # гость заходит на этот путь.
        self.assertEqual(result.status_code, HTTPStatus.OK) # проверка: код после перехода равен коду 200 (статус ОК).



class TestNewsPage(TestCase):
    """
    Тесты для проверки страницы новостей
    """
    fixtures = {
        'authapp/fixtures/001_user_admin.json',
        'mainapp/fixtures/001_news_fixt.json'
    } # фикстуры моделей, которые будут использоваться в тесте

    def setUp(self):  # логин воображаемого пользователя
        """
        Логина виртуального пользователя, который случается при каждом тесте. Подробные характеристики пользователя
        в фикстуре, ссылка на которую выше
        """
        super().setUp() # наследуем
        self.client_with_auth = Client() # экземпляр класса Клиент - специальный класс для виртуального пользователя
        path_auth = reverse('authapp_namespace:login') # переходим к странице логина
        self.client_with_auth.post(path_auth, data={'username': 'admin',
                                                    'password': 'admin'}) # вводим данные логина, которые в фикстуре

    def test_page_open(self):
        """
        Открытие страницы новостей
        """
        path = reverse('mainapp_namespace:news_list') # путь к странице новостей
        result = self.client.get(path)# виртуальный пользователь переходит по пути
        self.assertEqual(result.status_code, HTTPStatus.OK)# результат с обоих сторон должен быть 200

    def test_page_open_detail(self):
        """
        Открытие деталей новостей
        """
        news_obj = News.objects.first() # берем в качестве примера первую новость из БД
        path = reverse('mainapp_namespace:news_detail', args=[news_obj.pk]) # путь к деталям первой новости
        result = self.client.get(path) # виртуальный пользователь переходит по пути
        self.assertEqual(result.status_code, HTTPStatus.OK) # результат с обоих сторон должен быть 200

    def test_page_open_create_deny_access(self):
        """
        Защита от создания новостей неавторизованными пользователями
        """
        path = reverse('mainapp_namespace:news_create') # путь к созданию новости НЕ модератором
        result = self.client.get(path)# виртуальный пользователь переходит по пути
        self.assertEqual(result.status_code, HTTPStatus.FOUND) # результат должен быть 302 (редирект)

    def test_page_open_create_by_admin(self):
        """
        Открытие страницы создания новостей модераторами
        """
        path = reverse('mainapp_namespace:news_create')# путь к созданию новости модератором
        result = self.client_with_auth.get(path)# модератор или суперпользователь переходит по пути
        self.assertEqual(result.status_code, HTTPStatus.OK)# результат с обоих сторон должен быть 200

    def test_create_in_web(self):
        """
        Создание новостей модератором
        """
        counter_before = News.objects.count()# количество объектов новостей в БД
        path = reverse('mainapp_namespace:news_create') # путь к странице создания новости
        self.client_with_auth.post(
            path,
            data={
                'title': 'NewTestNews001',
                'preambule': 'NewTestNews001',
                'body': 'NewTestNews001'
            }
        ) # модератор или суперпользователь отправляет данные для создания новости
        self.assertGreater(News.objects.count(), counter_before) # количество новостей после операции должно быть больше

    def test_page_open_update_deny_access(self):
        """
        Защита от изменения новостей неавторизованными пользователями
        """
        news_obj = News.objects.first()# первая новость из бД для примера
        path = reverse('mainapp_namespace:news_update', args=[news_obj.pk]) # путь к изменению этой новости
        self.assertEqual(result.status_code, HTTPStatus.FOUND) # должен быть ответь 302 ( редирект)

    def test_page_open_update_by_admin(self):
        """
        Открытие страницы изменения новостей модераторами
        """
        news_obj = News.objects.first()# первая новость из бД для примера
        path = reverse('mainapp_namespace:news_update', args=[news_obj.pk])# путь к изменению этой новости
        result = self.client_with_auth.get(path) # переход модератора или рута по пути
        self.assertEqual(result.status_code, HTTPStatus.OK) # должен быть ответ 200

    def test_update_in_web(self):
        """
        Изменение новостей (модератором)
        """
        new_title = 'NewsTestTitle0001' # название для новости, которую будем создавать
        news_obj = News.objects.first()# первая новость из БД для пример
        self.assertNotEqual(news_obj.title, new_title) # название новой новости и новости из БД должны отличаться
        path = reverse('mainapp_namespace:news_update', args=[news_obj.pk])# путь к изменению этой новости
        result = self.client_with_auth.post(
            path,
            data={
                'title': new_title,
                'preambule': news_obj.preambule,
                'body': news_obj.body
            }
        )# модератор или суперзер отправляет данные для изменения ноовости
        self.assertEqual(result.status_code, HTTPStatus.FOUND) # должен быть код 302 (редирект)
        news_obj.refresh_from_db() # обновляем данные бд
        self.assertEqual(news_obj.title, new_title) # имя новости в БД должно соответствовать тому, которое мы туда отправили

    def test_delete_deny_access(self):
        """
        Защита от удаления новостей неавторизованными пользователями
        """
        news_obj = News.objects.first()# первая новость из БД для пример
        path = reverse('mainapp_namespace:news_delete', args=[news_obj.pk])# путь к удалению этой новости
        result = self.client.post(path)# путь неавторизованного или НЕмодератора юзера к странице удаения
        self.assertEqual(result.status_code, HTTPStatus.FOUND) # страница не должна открыться

    def test_delete_in_web(self):
        """
        Удаление новости модератором
        """
        news_obj = News.objects.first()# первая новость из БД для пример
        path = reverse('mainapp_namespace:news_delete', args=[news_obj.pk])# путь к удалению этой новости
        response = self.client_with_auth.post(path)# переход модератора по пути
        news_obj.refresh_from_db() # обновляем объект в базе данны
        self.assertTrue(news_obj.deleted) # поле объекта deleted должно быть True


def is_redis_available():
    """
    Проверка включен Redis или нет
    """
    try:
        client = redis.StrictRedis(host='localhost', port=6379, db=0) #экземпляр класса для редиса (на вход подаются данные хранилища)
        client.ping() # сигнал для редиса (при включенном редисе должен отработать без ошибо)
        return True# редис включен
    except redis.ConnectionError:
        return False# редис выкл


class TestCoursesWithMock(TestCase):
    """
    Консервация объектов
    """
    fixtures = {
        "authapp/fixtures/001_user_admin.json",
        "mainapp/fixtures/002_course_fixt.json",
        "mainapp/fixtures/003_lesson_fixt.json",
        "mainapp/fixtures/004_courseteachers_fixt.json"
    }

    @skipUnless(is_redis_available(), 'Redis is not available')
    def test_page_open_detail(self):  # для успешного выполнения теста надо включить редис!
        """
        Тест открытия деталей новостей из мок объекта
        """
        course_obj = Courses.objects.first()
        path = reverse('mainapp_namespace:courses_details', args=[course_obj.pk])
        with open('mainapp/fixtures/006_feedback_list_9.bin', 'rb') as inpf, \
                mock.patch('django.core.cache.cache.get') as mocked_cache:
            mocked_cache.return_value = pickle.load(inpf)
            print(mocked_cache.called)
            result = self.client.get(path)
            self.assertEqual(result.status_code, HTTPStatus.OK)
            self.assertTrue(mocked_cache.called)


class TestCoursesPage(TestCase):
    """
    Открытие страницы курсов
    """
    fixtures = {
        'mainapp/fixtures/002_course_fixt.json',
        'authapp/fixtures/001_user_admin.json'
    }

    def setUp(self):
        """
        Логин виртуального пользователя, который случается при каждом тесте. Подробные характеристики пользователя
        в фикстуре, ссылка на которую выше
        """
        super().setUp()

        self.client_with_auth = Client()# экземпляр специального класса Client()

        path_auth = reverse('authapp_namespace:login') # переход на страницу логина
        self.client_with_auth.post(path_auth, data={'username': 'admin',
                                                    'password': 'admin'}) # отправка данных для входа (указаны в фикстуре)
    def test_page_open_courses_list(self):
        """
        Открытие страницы курсов
        """
        path = reverse('mainapp_namespace:courses_page')
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_open_detail_course(self):
        """
        Открытие деталей курсов
        """
        all_courses = Courses.objects.all()
        for course in all_courses:
            path = reverse('mainapp_namespace:courses_details', args=[course.pk])
            result = self.client.get(path)
            self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_pay_course(self):
        """
        Открытие деталей одного курса
        """
        course = Courses.objects.first()
        path = reverse('mainapp_namespace:courses_details', args=[course.pk])
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_pay_new_course_auth_user(self):
        """
        Покупка нового курса (добавление курса в поле purchased_courses виртуального юзера
        """
        course = Courses.objects.first()
        self.assertIsNotNone(course, 'Course should exist')  # проверка существования
        path = reverse('authapp_namespace:add_course', args=[course.pk])
        user = get_user_model().objects.get(username='admin')
        counter_before = user.purchased_courses.count()
        self.client_with_auth.get(path)  # подходит и для get_user_model
        counter_after = user.purchased_courses.count()
        self.assertGreater(counter_after, counter_before)

    def test_pay_already_user_course(self):
        """
        Покупка курса, который уже был куплен
        """
        course = Courses.objects.first()
        self.assertIsNotNone(course, 'не существует курса')

        user = get_user_model().objects.get(username='admin')
        user.purchased_courses.add(course)  # добавляем в ручную курс
        counter_before = user.purchased_courses.count()

        path = reverse('authapp_namespace:add_course', args=[course.pk])  # url добавления курса
        self.client_with_auth.get(path)  # переходим

        counter_after = user.purchased_courses.count()
        self.assertEqual(counter_after, counter_before)  # количество курсов в созданного юзера не должно измениться


class TestUserDate(TestCase):
    """
    Класс тестирования данных пользователя
    """
    fixtures = {
        'authapp/fixtures/001_user_admin.json'
    }

    def setUp(self):
        """
        См. выше, что это
        """
        super().setUp()
        self.client_with_auth = Client()
        path_auth = reverse('authapp_namespace:login')
        self.client_with_auth.post(path_auth, data={'username': 'admin',
                                                    'password': 'admin'})

    def test_page_open_edit_profile(self):
        """
        Редактирование учетной записи
        """

        user = get_user_model().objects.get(username='admin')
        path = reverse('authapp_namespace:profile_edit', args=[user.pk])
        result = self.client_with_auth.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_page_open_my_course(self):
        """
        Просмотр купленных курсов
        """
        path = reverse('authapp_namespace:view_courses')
        result = self.client_with_auth.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_page_open_admin_panel(self):
        """
        Открытие админ панели
        """
        path = reverse('admin:index')
        result = self.client_with_auth.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)


class TestCRUDSelenium(StaticLiveServerTestCase):
    """
    Класс тестов для Selenium (утилита, которая сама работает в браузере)
    """
    fixtures = {
        'authapp/fixtures/001_user_admin.json',
        'mainapp/fixtures/001_news_fixt.json'
    }

    def setUp(self):
        """
        См. выше, что это
        """
        super().setUp()
        self.selenium = WebDriver() # Создаем драйвер
        self.selenium.implicitly_wait(10) # Какая то обязательная штука (время). Потом подробнее опишу, что это
        # self.test_login_by_selenium()

    def test_login_by_selenium(self):
        """
        Вспомогательный метод. Selenium логинится, записывая соответствующие данные в найденные поля
        """
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

    def _login_and_size(self):
        """
        Функция, вызывающая метод логина и устанавливающая нужный нам размер окна
        """
        self.test_login_by_selenium()
        self.selenium.set_window_size(1710, 1112)

    # @skip # декоратор, если тест нужно пропустить
    def test_CRUD_create(self):
        """
        Проверка работы Selenium для Create новостей
        """
        self._login_and_size()
        self.selenium.get(f'{self.live_server_url}{reverse("mainapp_namespace:news_create")}')  # переходим к странице создания новости
        self.selenium.find_element(By.NAME, 'title').send_keys('Тестовая новость из селениума')  # находим элемент
        self.selenium.find_element(By.NAME, 'preambule').send_keys('Тестовое описание из селениума')  # находим элемент
        self.selenium.find_element(By.NAME, 'body').send_keys(f'Тестовое тело новости из селениума')  # находим элемент
        button_post = WebDriverWait(self.selenium, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Опубликовать']"))
        )  # находи элемент (кнопку публикации новости)
        print(f'кнопка кликабельна') if button_post.is_displayed() and button_post.is_enabled() else print(
            f'не кликабельна')

        button_post.click()  # кликаем ее

        time.sleep(2)  # спец. пауза - во время теста добавить новость в БД и отрисовать страницу с новостями (редирект)
        self.assertIn('Тестовая новость из селениума',
                      self.selenium.page_source)  # проверяем наличие заглавия новости в списке новостей

    # @skip
    def test_CRUD_read(self):
        """
        Проверка работы Selenium для Read новостей
        """
        self._login_and_size()
        self.selenium.get(f'{self.live_server_url}{reverse("mainapp_namespace:news_detail", args=[2])}')
        time.sleep(2)
        detail_news_2 = News.objects.get(id=2).body
        self.assertIn(detail_news_2, self.selenium.page_source)

    # @skip
    def test_CRUD_update(self):
        """
        Проверка работы Selenium для Update новостей
        """
        self._login_and_size()
        print(News.objects.get(id=8))
        last_news = News.objects.latest('id').id

        self.selenium.get(f'{self.live_server_url}{reverse("mainapp_namespace:news_update", args=[last_news])}')
        time.sleep(2)
        body_ship = self.selenium.find_element(By.NAME, 'body')
        button_update = WebDriverWait(self.selenium, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Опубликовать']"))
        )

        body_ship.send_keys(f'Дополнительная информация от selenium')
        time.sleep(2)
        button_update.click()
        time.sleep(2)
        self.selenium.get(f'{self.live_server_url}{reverse("mainapp_namespace:news_detail", args=[last_news])}')
        self.assertIn('Дополнительная информация от selenium', self.selenium.page_source)

    # @skip
    def test_CRUD_delete(self):
        """
        Проверка работы Selenium для Delete новостей
        """
        self._login_and_size()
        last_news_id = News.objects.latest('id').id
        last_news_body = News.objects.latest('id').body
        self.selenium.get(f'{self.live_server_url}{reverse("mainapp_namespace:news_list")}')
        time.sleep(2)
        self.selenium.get(f'{self.live_server_url}{reverse("mainapp_namespace:news_delete", args=[last_news_id])}')
        button_delete = WebDriverWait(self.selenium, 10).until(EC.element_to_be_clickable(
            (By.XPATH, "//button[text()='Подтвердить']")))
        time.sleep(2)
        button_delete.click()
        time.sleep(2)
        self.assertNotIn(last_news_body, self.selenium.page_source)
    def test_change_language(self):
        """
        Проверка работы Selenium для изменения языка
        """
        self._login_and_size()

        button_language_uk = WebDriverWait(self.selenium, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn-link' and text()='🇬🇧']"))
        )

        time.sleep(2)
        button_language_uk.click()
        time.sleep(2)
        self.assertIn(f'News', self.selenium.page_source)

    def tearDown(self):
        """
        Закрытие браузера, открытого с помощью Selenium
        """
        if self.selenium:
            self.selenium.quit()
        super().tearDown()


class TestTaskMailSend(TestCase):
    """
    Проврка отправки писем
    """

    fixtures = {"authapp/fixtures/001_user_admin.json"}

    def test_mail_send(self):
        message_text = 'test_message_text'
        user_obj = authapp.models.CustomUser.objects.first()
        mainapp.tasks.send_feedback_mail(
            {'user_id': user_obj.id,
             'message': message_text}
        )
        self.assertEqual(django_mail.outbox[0].body, message_text)
