# Generated by Django 3.2.24 on 2024-03-17 18:05

from django.db import migrations
from random import randint
def forwards_func(apps, schema_editor):
    Lesson = apps.get_model('mainapp', 'Lesson')
    Courses = apps.get_model('mainapp', 'Courses')
    id_inc = 1
    course_quantity = len(Courses.objects.all())
    #Пусть будет 9 курсов, в каждом будет от 8 до 11 уроков
    for course_id in range(1, course_quantity + 1):
        for number_lesson in range(1, randint(9, 12)):
            Lesson.objects.create(
                id = id_inc,
                course = Courses.objects.get(id=course_id),
                num = number_lesson,
                title = f'урок № {number_lesson}',
                description = f'Подробное описание {number_lesson}-го урока.'
            )
            id_inc += 1

def reverse_func(apps, schema_editor):
    Lesson = apps.get_model('mainapp', 'Lesson')
    Lesson.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_migration_id_9'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func)
        ]