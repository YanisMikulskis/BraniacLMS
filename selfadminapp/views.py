from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import UpdateView, CreateView
from django.urls import reverse_lazy
import os

from mainapp.models import Courses, News, Lesson, CourseTeachers
from authapp.models import CustomUser

from django.views.generic import TemplateView


# def get_models():
#     print(os.getcwd())
# get_models()


class SelfAdminPanel(TemplateView):
    template_name = 'self_admin_template.html'

    def get_context_data(self, pk=None, **kwargs):
        context = super().get_context_data(pk=pk, **kwargs)
        context['Courses'] = Courses.objects.all()
        context['News'] = News.objects.all()
        context['Lesson'] = Lesson.objects.all()
        context['CourseTeachers'] = CourseTeachers.objects.all()
        context['CustomUser'] = CustomUser.objects.all()
        context['select'] = None
        # context['Courses'] = get_object_or_404(Courses, pk=pk)
        # context['News'] = get_object_or_404(News, pk=pk)
        # context['Lesson'] = get_object_or_404(Lesson, pk=pk)
        # context['CourseTeachers'] = get_object_or_404(CourseTeachers, pk=pk)
        # context['CustomUser'] = get_object_or_404(CustomUser, pk=pk)
        return context


class CourseUpdateView(PermissionRequiredMixin, UpdateView):
    model = Courses
    fields = '__all__'
    success_url = reverse_lazy("selfadminapp_namespace:admin_custom")
    permission_required = ("selfadminapp.update_course",)


class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    model = News
    fields = '__all__'
    success_url = reverse_lazy("selfadminapp_namespace:admin_custom")
    permission_required = ("selfadminapp.update_news",)

class TeacherUpdateView(PermissionRequiredMixin, UpdateView):
    model = CourseTeachers
    fields = '__all__'
    success_url = reverse_lazy("selfadminapp_namespace:admin_custom")
    permission_required = ("selfadminapp.update_teachers",)

class CourseCreateView(PermissionRequiredMixin, CreateView):
    model = Courses
    fields = '__all__'
    success_url = reverse_lazy("selfadminapp_namespace:admin_custom")
    permission_required = ("selfadminapp.create_course")

    # class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    #     model = mainapp_models.News
    #     fields = "__all__"
    #     success_url = reverse_lazy("mainapp_namespace:news")
    #     permission_required = ("mainapp.change_news",)
# Create your views here.
