from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import BooleanField


class StyleFormMixin:
    """ Миксин для формы стилей. """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['email', 'password1', 'password2']
