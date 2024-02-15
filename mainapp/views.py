from datetime import datetime
from typing import Any

from django.views.generic import TemplateView


class MainPageView(TemplateView):
    template_name = "mainapp/index.html"


class NewsPageView(TemplateView):
    template_name = "mainapp/news.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["news_title"] = "Zagolovok_test"
        context["news_preview"] = "Opisanie_test"
        context["range"] = range(1, 6)
        context["datetime_obj"] = datetime.now()
        context["test_title"] = "Test_zagolovok"
        context["test_preview"] = "Test_opisanie"
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
        context["page_num"] = page
        # context["range_pag"] = range(1,6) if page == 1 else range(6, 12)
        dict_page = {1: range(1, 6), 2: range(6, 11), 3: range(11, 16), 4: range(16, 21), 5: range(21, 23)}
        context["range_pag"] = dict_page[page]
        return context
