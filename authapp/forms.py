from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.utils.translation import gettext_lazy as _

class CustomUserCreationForm(UserCreationForm):
    field_order = [
        "username",
        "password1",
        "password2",
        "email",
        "first_name",
        "last_name",
        "age",
        "avatar",
    ]

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "email",
            "last_name",
            "first_name",
            "age",
            "avatar",
        )
        field_classes = {"username": UsernameField}