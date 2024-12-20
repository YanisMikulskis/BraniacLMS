# Create your models here.
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
class News(models.Model):
    title = models.CharField(max_length=256, verbose_name=_('Заголовок новости'))
    preambule = models.CharField(max_length=1024, verbose_name=_('Описание новости'))
    body = models.TextField(blank=True, null=True, verbose_name=_('Текст новости'))
    body_as_markdown = models.BooleanField(default=False, verbose_name='Разметка markdown')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Created verbose', editable=False)
    updated = models.DateTimeField(auto_now=True, verbose_name='Update_verbose', editable=False)
    deleted = models.BooleanField(verbose_name='Удаленная новость', default=False)

    def __str__(self):
        return f'{self.pk}  {self.title}'

    def delete(self, *args):
        self.deleted = True
        self.save()
    class Meta:
        verbose_name = _('News')
        verbose_name_plural = _('News')
        ordering = ('-created',)

class Courses(models.Model):
    name = models.CharField(max_length=256, verbose_name='name')
    description = models.TextField(blank=1, null=1, verbose_name='Description')
    description_as_markdown = models.BooleanField(default=False, verbose_name='As markdown')
    cost = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Cost')
    cover = models.CharField(max_length=25, default='no_image.svg', verbose_name='Cover')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    updated = models.DateTimeField(auto_now=True, verbose_name='Updated')
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.pk}:{self.name}'

    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.save()

    class Meta:
        verbose_name = _('Courses')
        verbose_name_plural = verbose_name
        ordering=['pk']



class Lesson(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    num = models.PositiveIntegerField(verbose_name='Lesson_number')
    title = models.CharField(max_length=256, verbose_name='Name')
    description = models.TextField(blank=True, null=True, verbose_name='Description')
    description_as_markdown = models.BooleanField(default=False, verbose_name='As markdown')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Created', editable=False)
    update = models.DateTimeField(auto_now=True, verbose_name='Updated', editable=False)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.course.name} | {self.num}: {self.title}'

    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.save()

    class Meta:
        verbose_name = _('Lesson')
        verbose_name_plural = _('Lessons')
        ordering = ('course', 'num')


class CourseTeachers(models.Model):
    course = models.ManyToManyField(Courses)
    name_teacher = models.CharField(max_length=128, verbose_name='Name teacher')
    surname_teacher = models.CharField(max_length=128, verbose_name='Surname teacher')
    day_birth = models.DateField(verbose_name='BD')
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.pk}: {self.name_teacher} {self.surname_teacher}'

    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.save()

    class Meta:
        verbose_name = _('CourseTeachers')
        verbose_name_plural = verbose_name
        ordering = ['pk']

class Intermediate(models.Model):
    teacher_inter = models.ForeignKey(to=CourseTeachers, on_delete=models.CASCADE)
    course_inter = models.ForeignKey(to=Courses, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.teacher_inter}: курсы: {self.course_inter}'


class DataTransfer(models.Model):
    title_transfer = models.CharField(max_length=256, verbose_name='Title_verbose')
    preambule_transfer = models.CharField(max_length=1024, verbose_name='Preambule_verbose')
    body_transfer = models.TextField(blank=True, null=True, verbose_name='Body_verbose')
    body_as_markdown_transfer = models.BooleanField(default=False, verbose_name='As markdown verbose')
    created_transfer = models.DateTimeField(auto_now_add=True, verbose_name='Created verbose', editable=False)
    updated_transfer = models.DateTimeField(auto_now=True, verbose_name='Update_verbose', editable=False)
    deleted_transfer = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.pk}  {self.title_transfer}'

    def delete(self, *args):
        self.deleted_transfer = True
        self.save()

class CourseFeedback(models.Model):
    RATING = ((5, "Отлично"),
              (4, "Хорошо"),
              (3, "Удовлетворительно"),
              (2, "Плохо"),
              (1, "Очень плохо"))
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, verbose_name=_('Course'))
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_('User'))
    feedback = models.TextField(default=_('No feedback'), verbose_name=_('Feedback'))
    rating = models.SmallIntegerField(choices=RATING, default=5, verbose_name=_('Rating'))
    created = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.course} ({self.user})'


class TestTable(models.Model):
    name = models.CharField(max_length=100, verbose_name='Test_name')