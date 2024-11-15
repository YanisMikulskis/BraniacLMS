# Generated by Django 5.0.6 on 2024-08-25 20:56

from django.db import migrations

def forward_func(apps, schema_editor):
    News = apps.get_model('mainapp', 'News')
    new_news = News.objects.get(id=3)
    new_news.preambule = 'Zoom снова актуален! Приходите заниматься'
    new_news.save()




def reverse_func(apps, schema_editor):
    ...


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0021_testtable_alter_coursefeedback_rating'),
    ]

    operations = [
        migrations.RunPython(forward_func, reverse_func)
    ]
