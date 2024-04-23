from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.http import HttpResponse

class CustomLoginView(LoginView):
    def form_valid(self, form): #форма верного входа пользователя
        ret = super().form_valid(form)

        message = _("Login success!<br>Hi, %(username)s") % {
        "username": self.request.user.get_full_name() if self.request.user.get_full_name()
        else self.request.user.get_username()
        }
        messages.add_message(self.request, messages.INFO, mark_safe(message))
        return ret

    def form_invalid(self, form): #форма неверного входа пользователя
        for _unused, msg in form.error_messages.items():
            messages.add_message(self.request, messages.WARNING, mark_safe(f"Something goes wrong:<br>{msg}"),
                                 )

        return self.render_to_response(self.get_context_data(form=form))

class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.add_message(self.request, messages.INFO, _('See you later'))
        return super().dispatch(request, *args, **kwargs)



# Create your views here.
 