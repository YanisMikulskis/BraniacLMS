import os

from django.contrib import messages
from django.contrib.auth import logout, login, get_user_model
from django.shortcuts import redirect

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, CreateView

from django.http import HttpResponse
from authapp import models, forms
from .forms import CustomUserCreationForm

from .models import CustomUser

from mainapp.models import Courses


class CustomLoginView(LoginView):

    def form_valid(self, form):
        context = super().form_valid(form)
        if not self.request.user.is_superuser:
            if self.request.user.get_full_name():
                self.name = self.request.user.get_full_name()
            else:
                self.name = self.request.user.get_username()
        else:
            self.name = 'ROOT!'
        message = f"Login success!<br> Hello, dear {self.name}"

        messages.add_message(self.request, messages.INFO, mark_safe(message))
        return context

    def form_invalid(self, form):
        for _unused, msg in form.error_messages.items():
            messages.add_message(
                self.request,
                messages.WARNING,
                mark_safe(f"Something goes wrong:<br>{msg}"),
            )
        return self.render_to_response(self.get_context_data(form=form))

def logout_view(request):

    name_user = request.user if not request.user.is_superuser else 'ROOT!'

    message = f'See you later, dear {name_user}'
    messages.add_message(request, messages.INFO, mark_safe(message))
    logout(request)
    return redirect('/')



class RegisterView(CreateView):
    model = get_user_model()
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("mainapp_namespace:main_page")


    # template_name = "registration/register.html"
    #
    # def post(self, request, *args, **kwargs):
    #     try:
    #         if all(
    #                 (
    #                         request.POST.get("username"),
    #                         request.POST.get("email"),
    #                         request.POST.get("password1"),
    #                         request.POST.get("password1") == request.POST.get("password2"),
    #                 )
    #         ):
    #             new_user = models.CustomUser.objects.create(
    #                 username=request.POST.get("username"),
    #                 first_name=request.POST.get("first_name"),
    #                 last_name=request.POST.get("last_name"),
    #                 age=request.POST.get("age") if request.POST.get("age") else f'Скрыт',
    #                 avatar=request.FILES.get("avatar"),
    #                 email=request.POST.get("email"),
    #             )
    #             new_user.set_password(request.POST.get("password1"))
    #             new_user.save()
    #             messages.add_message(request, messages.INFO, _("Registration success!"))
    #             return HttpResponseRedirect(reverse_lazy("authapp_namespace:login"))
    #     except Exception as exp:
    #         messages.add_message(
    #             request,
    #             messages.WARNING,
    #             mark_safe(f"Something goes wrong:<br>{exp}"),
    #         )
    #         return HttpResponseRedirect(reverse_lazy("authapp_namespace:register"))


class ProfileEditView(LoginRequiredMixin, TemplateView):
    template_name = "registration/profile_edit.html"
    login_url = reverse_lazy("authapp_namespace:login")

    def post(self, request, *args, **kwargs):
        try:
            if request.POST.get("username"):
                request.user.username = request.POST.get("username")
            if request.POST.get("first_name"):
                request.user.first_name = request.POST.get("first_name")
            if request.POST.get("last_name"):
                request.user.last_name = request.POST.get("last_name")
            if request.POST.get("age"):
                request.user.age = request.POST.get("age")
            if request.POST.get("email"):
                request.user.email = request.POST.get("email")
            if request.FILES.get("avatar"):
                if request.user.avatar and os.path.exists(request.user.avatar.path):
                    os.remove(request.user.avatar.path)
                request.user.avatar = request.FILES.get("avatar")
            request.user.save()
            messages.add_message(request, messages.INFO, _(f'Data saved!'))
        except Exception as exp:
            messages.add_message(request,
                                 messages.WARNING,
                                 mark_safe(f'Error <br> {exp}'),
                                 )
        return HttpResponseRedirect(reverse_lazy(f"authapp_namespace:profile_edit"))


#
class RemoveCourse(TemplateView):
    template_name = "courses/remove_course.html"

    def remove_course(self, pk):
        self.current_course = Courses.objects.get(id=pk)
        self.current_user.purchased_courses.remove(self.current_course)

    def get_context_data(self, pk=None, **kwargs):
        context = super().get_context_data(pk=pk, **kwargs)
        self.current_user = CustomUser.objects.get(id=self.request.user.id)
        self.remove_course(pk)
        context['remove_course'] = self.current_course
        return context


class MyCourses(TemplateView):
    # template_name = "courses/my_courses.html"
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.template_name = "courses/my_courses.html"

    def get_context_data(self, pk=None, **kwargs):
        context = super().get_context_data(pk=pk, **kwargs)
        self.current_user = CustomUser.objects.get(id=self.request.user.id)
        my_courses = self.current_user.purchased_courses.all()
        context['my_courses'] = my_courses
        return context


class Add_Courses(TemplateView):
    template_name = "courses/add_courses_info.html"
    def add(self, id_course):
        request = self.request
        self.current_user = CustomUser.objects.get(id=request.user.id)
        self.current_course = Courses.objects.get(id=id_course)
        self.all_courses = self.current_user.purchased_courses.all()
        if self.current_course not in self.all_courses:
            self.current_user.purchased_courses.add(self.current_course)
            return True
        else:
            return False

    # def get_template_names(self, *template):
    #     # if self.result_add:
    #     if not self.temp:
    #         return ['courses/add_courses_info.html']
    #     else:
    #         return ['registration/profile_edit.html']

    # 'courses/my_courses.html'

    def get_context_data(self, pk=None, **kwargs):
        context = super().get_context_data(pk=pk, **kwargs)
        self.result_add = self.add(pk)
        context['result_add'] = self.result_add
        if self.result_add:
            context['current_user'] = self.current_user
            context['courses_user'] = self.current_course.name
            return context
        else:
            message = 'Этот курс уже добавлен! Зайдите в "Мои курсы".'
            messages.add_message(self.request, messages.WARNING, mark_safe(message))


