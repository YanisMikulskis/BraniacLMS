from django.urls import path
from django.views.decorators.cache import cache_page

from . import views
from .apps import MainappConfig

app_name = MainappConfig.name

urlpatterns = [
    path("", views.MainPageView.as_view(), name="main_page"),
    path("news/", views.NewsListView.as_view(), name="news_list"),
    path("news/create/", views.NewsCreateView.as_view(), name="news_create"),
    path("news/<int:pk>/detail", views.NewsDetailView.as_view(), name="news_detail"),
    path("news/<int:pk>/update", views.NewsUpdateView.as_view(), name="news_update"),
    path("news/<int:pk>/delete", views.NewsDeleteView.as_view(), name="news_delete"),

    # path("course/<int:pk>/update", views.CourseUpdateView.as_view(), name='course_update'),

    # path("news/", views.NewsListView.as_view(), name="news_page"),
    # path("news/<int:page>/", views.NewsWithPaginatorView.as_view(), name="news_paginator"),
    # path("page/<int:pk>/", views.NewPageDetailView.as_view(), name="detail_news"),
    path("courses/", views.CoursesListView.as_view(), name="courses_page"),
    path("courses/<int:pk>/", views.CoursesDetailView.as_view(), name="courses_details"),
    path("contacts/", views.ContactsPageView.as_view(), name="contacts_page"),
    path("doc_site/", views.DocSitePageView.as_view(), name="doc_page"),
    path("test_page/", views.TestPageView.as_view(), name="test_page_for_namespace"),
    path("course_feedback/", views.CourseFeedbackFormProcessView.as_view(), name="course_feedback"),
    path("log_view/", views.LogView.as_view(), name='log_view'),
    path("log_download/", views.LogDownloadView.as_view(), name='log_download')
]

