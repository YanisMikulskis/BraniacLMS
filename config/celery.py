from __future__ import absolute_import, unicode_literals

import os
from celery import Celery

#Для начала нужно установить значение по умолчанию для среды DJANGO_SETTINGS_MODULE,
# чтобы Celery знала, как найти проект Django.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
# Затем мы создали экземпляр Celery с именем braniac и поместили в переменную celery_app.
celery_app = Celery('braniac')
# Затем мы загрузили значения конфигурации Celery из объекта
# настроек из django.conf. Мы использовали namespace=«CELERY»
# для предотвращения коллизий с другими настройками Django.
# Таким образом, все настройки конфигурации для Celery должны
# начинаться с префикса CELERY_
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
# Наконец, app.autodiscover_tasks() говорит Celery искать задания из
# приложений, определенных в settings.INSTALLED_APPS.
celery_app.autodiscover_tasks()