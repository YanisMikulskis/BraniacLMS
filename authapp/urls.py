from django.urls import path

from . import views
from .apps import AuthappConfig

from .models import CustomUser

app_name = AuthappConfig.name

from django.http import HttpResponse

urlpatterns = [
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("profile_edit/<int:pk>", views.ProfileEditView.as_view(), name="profile_edit"),
    path("my_courses/", views.MyCourses.as_view(), name="view_courses"),
    path("my_courses/<int:pk>", views.Add_Courses.as_view(), name="add_course"),
    path("remove_course/<int:pk>", views.RemoveCourse.as_view(), name="remove_course")

]
