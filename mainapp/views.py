import os
from datetime import datetime
from typing import Any
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import News, Courses, Lesson, CourseTeachers
from django.http import HttpResponse
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from mainapp import models as mainapp_models
from django.urls import reverse_lazy
from mainapp import forms
from django.template.loader import render_to_string
from django.http import JsonResponse
class MainPageView(TemplateView):
    template_name = "mainapp/index.html"


class NewsListView(ListView):
    model = mainapp_models.News
    paginate_by = 5
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)

class NewsCreateView(PermissionRequiredMixin, CreateView):
    model = mainapp_models.News
    fields = '__all__'
    success_url = reverse_lazy('mainapp_namespace:main_page')
    permission_required = ('mainapp.add_news',)

class NewsDetailView(DetailView):
    model = mainapp_models.News

class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    model = mainapp_models.News
    fields = "__all__"
    success_url = reverse_lazy("mainapp_namespace:news")
    permission_required = ("mainapp.change_news",)
class NewsDeleteView(PermissionRequiredMixin, DeleteView):
    model = mainapp_models.News
    success_url = reverse_lazy("mainapp_namespace:news")
    permission_required = ("mainapp.delete_news",)



# class NewsPageView(TemplateView):
#     template_name = "mainapp/news_list.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['news_qs'] = News.objects.all()[:6]
#         return context

#
# class NewPageDetailView(TemplateView):
#     template_name = 'mainapp/news_detail.html'
#
#     def get_context_data(self, pk=None, **kwargs):
#         context = super().get_context_data(pk=pk, **kwargs)
#         context['news_object'] = get_object_or_404(News, pk=pk)
#         context['current_page'] = NewsWithPaginatorView.back()
#         return context
#
#
# class NewsWithPaginatorView(NewsPageView):
#     page_by_class = 0
#
#     def get_context_data(self, page, **kwargs: Any) -> dict[str, Any]:
#         NewsWithPaginatorView.page_by_class = page  # введено для того, чтобы при нажатии на кнопку "Назад" мы
#         # возвращались на текущую страницу из пагинатора
#         context = super().get_context_data(page=page, **kwargs)
#         context["page_number"] = page
#         dict_page = {1: range(1, 6), 2: range(6, 11), 3: range(11, 16), 4: range(16, 21), 5: range(21, 25)}
#         context["previous_page"] = page - 1 if page > 1 else list(dict_page.keys())[-1]
#         context["next_page"] = page + 1 if page < 5 else list(dict_page.keys())[0]
#         context["range_for_news"] = dict_page[page]
#         context["paginator_range"] = range(1, 6)
#         return context
#
#     @classmethod
#     def back(cls):
#         return cls.page_by_class


class CoursesPageView(TemplateView):
    template_name = "mainapp/courses_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Courses'] = Courses.objects.all()
        return context


class CoursesDetailView(TemplateView):
    template_name = "mainapp/courses_detail.html"
    def get_context_data(self, pk=None, **kwargs):
        context = super().get_context_data(pk=pk, **kwargs)
        context['Courses'] = get_object_or_404(Courses, pk=pk)
        context['Teachers'] = CourseTeachers.objects.filter(course=context['Courses'])
        context['Lesson'] = Lesson.objects.filter(course=context['Courses'])
        if not self.request.user.is_anonymous:
            if not mainapp_models.CourseFeedback.objects.filter(
                course=context['Courses'], user = self.request.user).count():
                context['feedback_form'] = forms.CourseFeedbackForm(course=context['Courses'], user=self.request.user)
        context['Feedback_list'] = mainapp_models.CourseFeedback.objects.filter(
            course = context['Courses']).order_by('-created', '-rating')[:5]
        if context['Feedback_list']:
            medium_grade = mainapp_models.CourseFeedback.objects.filter(course=context['Courses']).values_list('rating')
            context['Medium_grade'] = sum([item[0] for item in medium_grade]) / len(medium_grade)
        else:
            context['Medium_grade'] = 0
            # context['Test cont'] = 'fasfdfsdf'
        return context

class CourseFeedbackFormProcessView(LoginRequiredMixin, CreateView):
    model = mainapp_models.CourseFeedback
    form_class = forms.CourseFeedbackForm
    def form_valid(self, form):
        self.object = form.save()
        rendered_card = render_to_string(
            'mainapp/includes/feedback_card.html', context={'item':self.object}
        )
        return JsonResponse({'card':rendered_card})





class ContactsPageView(TemplateView):
    template_name = "mainapp/contacts.html"


class DocSitePageView(TemplateView):
    template_name = "mainapp/doc_site.html"


class LoginPageView(TemplateView):
    template_name = "authapp/templates/registration/login.html"


class TestPageView(TemplateView):
    template_name = "mainapp/test_html.html"

