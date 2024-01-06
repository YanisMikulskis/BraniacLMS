from django.urls import path

from mainapp import views
from mainapp.apps import MainappConfig

app_name = MainappConfig.name

urlpatterns = [
    path("", views.MainPageView.as_view(), name="main_page"),
    path("news/", views.NewsPageView.as_view(), name="news_page"),
    path("news/<int:page>/", views.NewsWithPaginatorView.as_view(), name="news_paginator"),
    path("courses/", views.CoursesPageView.as_view(), name="courses_page"),
    path("contacts/", views.ContactsPageView.as_view(), name="contacts_page"),
    path("doc_site/", views.DocSitePageView.as_view(), name="doc_page"),
    path("login/", views.LoginPageView.as_view(), name="login_page"),
    path("test_page/", views.TestPageView.as_view(), name="test_page_for_namespace"),
]
