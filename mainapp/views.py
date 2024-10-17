import os
from datetime import datetime
from typing import Any
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView, View
from .models import News, Courses, Lesson, CourseTeachers
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from mainapp import models as mainapp_models
from django.urls import reverse_lazy
from mainapp import forms
from mainapp import tasks as mainapp_tasks
from django.template.loader import render_to_string
from django.http import JsonResponse, FileResponse
from django.conf import settings
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)
class MainPageView(TemplateView):
    template_name = "mainapp/index.html"


class NewsListView(ListView):
    model = mainapp_models.News
    logger.debug("Log news")
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

class CoursesListView(ListView):
    model = mainapp_models.Courses
    paginate_by = len(model.objects.all())
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)

# class CoursesPageView(TemplateView):
#     template_name = "mainapp/courses_list.html"
#
#     def get_context_data(self, **kwargs):
#         logger.debug(f"This is CoursePageView")
#         context = super().get_context_data(**kwargs)
#         context['Courses'] = Courses.objects.all()
#         return context


class CoursesDetailView(TemplateView):
    template_name = "mainapp/courses_detail.html"
    def get_context_data(self, pk=None, **kwargs):
        logger.debug("Yet another log message")
        context = super().get_context_data(pk=pk, **kwargs)
        context['Courses'] = get_object_or_404(Courses, pk=pk)
        context['Teachers'] = CourseTeachers.objects.filter(course=context['Courses'])
        context['Lessons'] = Lesson.objects.filter(course=context['Courses'])
        if not self.request.user.is_anonymous:
            if not mainapp_models.CourseFeedback.objects.filter(
                course=context['Courses'], user = self.request.user).count():
                context['feedback_form'] = forms.CourseFeedbackForm(course=context['Courses'], user=self.request.user)


        # cached_feedback = cache.get(f'feedback_list_{pk}')
        # #Для кэширования нужно снять комментарии с кода и включить редис!
        # #brew services start redis (для MacOS)
        # if not cached_feedback:
        context['Feedback_list'] = mainapp_models.CourseFeedback.objects.filter(
                course = context['Courses']).order_by('-created', '-rating')[:5]
            # cache.set(f'feedback_list_{pk}', context['Feedback_list'], timeout=300)
        # else:
        #     context['Feedback_list'] = cached_feedback


        if context['Feedback_list']:
            medium_grade = mainapp_models.CourseFeedback.objects.filter(course=context['Courses']).values_list('rating')
            context['Medium_grade'] = sum([item[0] for item in medium_grade]) / len(medium_grade)
        else:
            context['Medium_grade'] = 0
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context[f'message_form'] = forms.MailFeedbackForm(user=self.request.user)
        return context
    #redis-server & celery -A config worker -l INFO & python manage.py runserver

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            cache_log_flag = cache.get(f'mail_feedback_lock_{self.request.user.pk}')
            if not cache_log_flag:
                cache.set(f'mail_feedback_lock_{self.request.user.pk}', 'lock', timeout=60)
                messages.add_message(self.request, messages.INFO, _('mMessage sended'))
                mainapp_tasks.send_feedback_mail.delay({
                    'user_id': self.request.POST.get('user_id'),
                    'message': self.request.POST.get('message')
                }

                )
            else:
                messages.add_message(
                    self.request,
                    messages.WARNING,
                    _('You can send only one message per 1 minute')
                )


        return HttpResponseRedirect(reverse_lazy('mainapp_namespace:contacts_page'))




class DocSitePageView(TemplateView):
    template_name = "mainapp/doc_site.html"


class LoginPageView(TemplateView):
    template_name = "authapp/templates/registration/login.html"


class TestPageView(TemplateView):
    template_name = "mainapp/test_html.html"


class CourseUpdateView(PermissionRequiredMixin, UpdateView):
    model = mainapp_models.Courses
    fields = '__all__'
    success_url = reverse_lazy
    permission_required = ("mainapp.update_course",)

class CourseCreateView(PermissionRequiredMixin, CreateView):
    model = mainapp_models.Courses
    fields = '__all__'
    success_url = reverse_lazy
    permission_required = ("mainapp.create_course")

class LogView(TemplateView):
    template_name = 'mainapp/log_view.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user.get_username()
        log_slice = []
        with open(settings.LOG_FILE, 'r') as log_file:
            print(f'Размер ЛОГА {os.path.getsize(settings.LOG_FILE) // 1024} кб')

            # print(f'Количество строк ЛОГА {len(log_file.read())} шт')
            for number_line, line in enumerate(log_file):

                if number_line == 200:
                    break
                log_slice.insert(0, f'{current_user}: {line}')
        context['log'] = ''.join(log_slice)
        return context

class LogDownloadView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, *args, **kwargs):
        return FileResponse(open(settings.LOG_FILE, "rb"))



# def clean_cookie(request):
#     response = HttpResponse('Удаляем куки файл с заглавной буквой')
#     response.delete_cookie('django-Language')
#     return response