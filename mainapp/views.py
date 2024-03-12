from datetime import datetime
from typing import Any
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from .models import News

class MainPageView(TemplateView):
    template_name = "mainapp/index.html"


class NewsPageView(TemplateView):
    template_name = "mainapp/news.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_qs'] = News.objects.all()[:5]
        #
        #
        #
        # context["news_title"] = "Zagolovok_test"
        # context["news_preview"] = "Opisanie_test"
        # # context["page_number"] = page
        # #context["first_range"] = range(1, 6)
        # context["datetime_obj"] = datetime.now()
        # context["test_title"] = "Test_zagolovok"
        # context["test_preview"] = "Test_opisanie"
        return context


class CoursesPageView(TemplateView):
    template_name = "mainapp/courses_list.html"


class ContactsPageView(TemplateView):
    template_name = "mainapp/contacts.html"


class DocSitePageView(TemplateView):
    template_name = "mainapp/doc_site.html"


class LoginPageView(TemplateView):
    template_name = "mainapp/login.html"


class TestPageView(TemplateView):
    template_name = "mainapp/test_html.html"


class NewsWithPaginatorView(NewsPageView):
    def get_context_data(self, page, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(page=page, **kwargs)

        context["page_number"] = page
        dict_page = {1: range(1, 6), 2: range(6, 11), 3: range(11, 16), 4: range(16, 21), 5: range(21, 25)}
        context["previous_page"] = page - 1 if page > 1 else list(dict_page.keys())[-1]
        context["next_page"] = page + 1 if page < 5 else list(dict_page.keys())[0]
        context["range_for_news"] = dict_page[page]
        context["paginator_range"] = range(1, 6)
        return context

class NewPageDetailView(TemplateView):
    template_name = 'mainapp/news_detail.html'
    def get_context_data(self, pk= None, **kwargs):
        context = super().get_context_data(pk=pk, **kwargs)
        context['news_object'] = get_object_or_404(News, pk=pk)
        return context
