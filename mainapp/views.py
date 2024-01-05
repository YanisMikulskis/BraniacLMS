from django.views.generic import TemplateView


class MainPageView(TemplateView):
    template_name = "mainapp/index.html"


class NewsPageView(TemplateView):
    template_name = "mainapp/news.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["news_title"] = "Zagolovok_test"
        context["news_preview"] = "Opisanie_test"
        context["range"] = range(5)
        context["paginator_range"] = range(10)
        context["tags"] = [
            ["Vika", "One"],
            ["Suchka", "Two"],
            ["Brusnichka", "Three"],
            ["Kisulya", "Four"],
            ["Sraka", "Five"],
        ]
        return context


class CoursesPageView(TemplateView):
    template_name = "mainapp/courses_list.html"


class ContactsPageView(TemplateView):
    template_name = "mainapp/contacts.html"


class DocSitePageView(TemplateView):
    template_name = "mainapp/doc_site.html"


class LoginPageView(TemplateView):
    template_name = "mainapp/login.html"
