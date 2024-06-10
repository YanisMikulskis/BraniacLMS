# Register your models here.
from django.contrib import admin

from . import models as mainapp_models
@admin.register(mainapp_models.News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'preambule', 'body']
    search_fields = ['title', 'preambule', 'body']

@admin.register(mainapp_models.Courses)
class CoursesAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'cost', 'cover', 'deleted']

@admin.register(mainapp_models.Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_course_name', 'num', 'title', 'deleted']
    ordering = ['-course__name', '-num']
    list_per_page = 5
    list_filter = ['course', 'created', 'deleted']
    actions = ['mark_deleted']
    def get_course_name(self, obj):  # обращение к модели many to many
        return obj.course.name

    get_course_name.short_description = 'Course'

    def mark_deleted(self, request, queryset): # добавление собственных действий
        queryset.update(deleted=True)

    mark_deleted.short_description = ('Mark deleted')
@admin.register(mainapp_models.CourseTeachers)
class CourseTeachersAdmin(admin.ModelAdmin):
    list_display = ['name_teacher', 'deleted']
    search_fields = ['name_teacher', 'surname_teacher']




