# Register your models here.
from django.contrib import admin

from . import models as mainapp_models
@admin.register(mainapp_models.News)
class NewsAdmin(admin.ModelAdmin):
    pass

@admin.register(mainapp_models.Courses)
class CoursesAdmin(admin.ModelAdmin):
    pass

@admin.register(mainapp_models.Lesson)
class LessonAdmin(admin.ModelAdmin):
    pass


@admin.register(mainapp_models.CourseTeachers)
class CourseTeachersAdmin(admin.ModelAdmin):
    pass




