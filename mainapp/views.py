from datetime import datetime
from typing import Any
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from .models import News, Courses, Lesson, CourseTeachers
from django.http import HttpResponse
class MainPageView(TemplateView):
    template_name = "mainapp/index.html"


class NewsPageView(TemplateView):
    template_name = "mainapp/news.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_qs'] = News.objects.all()[:6]
        return context
class NewPageDetailView(TemplateView):
    template_name = 'mainapp/news_detail.html'
    def get_context_data(self, pk=None, **kwargs):
        context = super().get_context_data(pk=pk, **kwargs)
        context['news_object'] = get_object_or_404(News, pk=pk)
        context['current_page'] = NewsWithPaginatorView.back()
        return context
class NewsWithPaginatorView(NewsPageView):
    page_by_class = 0
    def get_context_data(self, page, **kwargs: Any) -> dict[str, Any]:
        NewsWithPaginatorView.page_by_class = page #введено для того, чтобы при нажатии на кнопку "Назад" мы
        #возвращались на текущую страницу из пагинатора
        context = super().get_context_data(page=page, **kwargs)
        context["page_number"] = page
        dict_page = {1: range(1, 6), 2: range(6, 11), 3: range(11, 16), 4: range(16, 21), 5: range(21, 25)}
        context["previous_page"] = page - 1 if page > 1 else list(dict_page.keys())[-1]
        context["next_page"] = page + 1 if page < 5 else list(dict_page.keys())[0]
        context["range_for_news"] = dict_page[page]
        context["paginator_range"] = range(1, 6)
        return context
    @classmethod
    def back(cls):
        return cls.page_by_class





class CoursesPageView(TemplateView):
    template_name = "mainapp/courses_list.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Courses'] = Courses.objects.all()
        return context

class CoursesDetailView(TemplateView):
    template_name = "mainapp/courses_detail.html"
    def get_context_data(self,pk=None, **kwargs):
        context = super().get_context_data(pk=pk, **kwargs)
        context["Courses"] = get_object_or_404(Courses, pk=pk)

        context["Teachers"] = CourseTeachers.objects.filter(course=context["Courses"])
        context["Lesson"] = Lesson.objects.filter(course=context["Courses"])
        # context["current_page"] = CoursesPageView.as_view()
        return context


class ContactsPageView(TemplateView):
    template_name = "mainapp/contacts.html"


class DocSitePageView(TemplateView):
    template_name = "mainapp/doc_site.html"


class LoginPageView(TemplateView):
    template_name = "mainapp/../authapp/templates/registration/login.html"


class TestPageView(TemplateView):
    template_name = "mainapp/test_html.html"






