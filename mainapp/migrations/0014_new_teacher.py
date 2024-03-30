# Generated by Django 3.2.24 on 2024-03-30 12:44

from django.db import migrations
from faker import Faker
from random import randint as rINT
from random import choice
def forwards_func(apps, schema_editor):
    Teacher = apps.get_model('mainapp', 'CourseTeachers')
    Courses = apps.get_model('mainapp', 'Courses')
    faker_ = Faker('ru-RU')
    db = faker_.date_of_birth()
    courses_list = [Courses.objects.get(id=item) for item in range(1, len(Courses.objects.all()) + 1)]
    teacher = Teacher.objects.create(
        id = 8,
        name_teacher = 'Иван',
        surname_teacher='Павлов',
        day_birth=f'{db.year}-{db.month}-{db.day}'
    )
    teacher.course.set([courses_list.pop(courses_list.index(choice(courses_list))) for _ in range(2)])
def reverser_func(apps, schema_editor):
    Teacher = apps.get_model('mainapp', 'CourseTeachers')
    Teacher.objects.all()[-1].delete()

class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0013_delete_datatransfer'),
    ]

    operations = [
        migrations.RunPython(
            forwards_func,
            reverser_func
        )
    ]
