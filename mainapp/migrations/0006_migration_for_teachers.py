# Generated by Django 3.2.24 on 2024-03-21 17:10

from django.db import migrations
from faker import Faker
from random import randint as rINT
from random import choice
from django.db import models
def forwards_func(apps, schema_editor):
    Teacher = apps.get_model('mainapp', 'CourseTeachers')
    Course = apps.get_model('mainapp', 'Courses')
    faker_ = Faker('ru-RU')
    id_inc = 1
    courses_list = [Course.objects.get(id=i) for i in range(1,len(Course.objects.all())+1)]
    for i in range(5):
        db = faker_.date_of_birth()
        teacher = Teacher.objects.create(
        id = id_inc,
        name_teacher = faker_.first_name_male(),
        surname_teacher = faker_.last_name_male(),
        day_birth = f'{db.year}-{db.month}-{db.day}'
        )
        range_courses = 2 if len(courses_list) > 1 else 1
        teacher.course.set([courses_list.pop(courses_list.index(choice(courses_list))) for _ in range(range_courses)])
        id_inc += 1


def reverse_func(apps, schema_editor):

    Teacher = apps.get_model('mainapp', 'CourseTeachers')
    Teacher.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_migration_for_lessons'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func)
    ]
