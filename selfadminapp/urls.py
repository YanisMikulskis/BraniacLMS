from django.urls import path
from . import views
from .apps import SelfadminappConfig
app_name = SelfadminappConfig.name

urlpatterns = [
     path("admin_custom/", views.SelfAdminPanel.as_view(), name='admin_custom'),
     path("course/<int:pk>/update", views.CourseUpdateView.as_view(), name='course_update'),
     path("news/<int:pk>/update", views.NewsUpdateView.as_view(), name='news_update'),
     path("teacher/<int:pk>/update", views.TeacherUpdateView.as_view(), name='teachers_update'),
     path("course/<int:pk>/create", views.CourseCreateView.as_view(), name='course_create'),
     path("news/<int:pk>/create", views.NewsCreateView.as_view(), name='news_create'),
     path("teacher/<int:pk>/create", views.TeacherCreateView.as_view(), name='teachers_create'),
     path("course_create/", views.CourseCreateView.as_view(), name='course_create')
]