# Create your models here.
from django.db import models

class News(models.Model):
    title = models.CharField(max_length=256, verbose_name='Title_verbose')
    preambule = models.CharField(max_length=1024, verbose_name='Preambule_verbose')
    body = models.TextField(blank=True, null=True, verbose_name='Body_verbose')
    body_as_markdown = models.BooleanField(default=False, verbose_name='As markdown verbose')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Created verbose', editable=False)
    updated = models.DateTimeField(auto_now=True, verbose_name='Update_verbose', editable=False)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.pk}  {self.title}'

    def delete(self, *args):
        self.deleted = True
        self.save()
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
        ordering = ('course', 'num')

class CourseTeachers(models.Model):
    course = models.ManyToManyField(Courses)
    name_teacher = models.CharField(max_length=128, verbose_name='Name teacher')
    surname_teacher = models.CharField(max_length=128, verbose_name='Surname teacher')
    day_birth = models.DateTimeField(verbose_name='BD')
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.pk}: {self.name_teacher} {self.surname_teacher}'

    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.save()

    class Meta:
        ordering = ('surname_teacher')