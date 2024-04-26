from django.urls import path

from . import views
from .apps import AuthappConfig

app_name = AuthappConfig.name

urlpatterns = [
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("profile_edit/", views.ProfileEditView.as_view(), name="profile_edit")
    # path("profile_edit/", views.)

]