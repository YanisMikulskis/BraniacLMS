# Generated by Django 5.0.6 on 2024-11-05 09:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0022_update_news'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lesson',
            options={'ordering': ('course', 'num'), 'verbose_name': 'Lesson', 'verbose_name_plural': 'Lessons'},
        ),
    ]
