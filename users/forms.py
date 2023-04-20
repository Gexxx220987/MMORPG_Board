from django import forms
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from random import randint
from django.core.cache import cache
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy


class CodeValidationError(ValidationError):
    pass


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label='Email')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    @staticmethod
    def send_code_confirmation(user, code):
        html_content = render_to_string(
            'users/signup_cofirmation_email.html',
            {
                'user': user,
                'link': reverse_lazy('users:signup_check_email',
                                     kwargs={'pk': user.pk}),
                'code': code,
            }
        )
        msg = EmailMultiAlternatives(
            subject=f"Код подтверждения email",
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        code = randint(1000, 9999)
        cache.set(f'code:{user.pk}', code, timeout=300)
        self.send_code_confirmation(user, code)
        return user


class ConfirmationSignUpForm(forms.ModelForm):
    code = forms.IntegerField(label='Код подтверждения')

    class Meta:
        model = User
        fields = [
            'code',
        ]

    def __init__(self, user_pk, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_pk = user_pk

    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data['code']
        number = cache.get(f'code:{self.user_pk}', None)
        if code == number:
            cleaned_data['user'] = User.objects.get(pk=self.user_pk)
        else:
            raise CodeValidationError({
                'code': 'Введён неверный код или срок действия кода истёк',
            })
        return cleaned_data


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        ),
        label='Имя пользователя'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        ),
        label='Пароль'
    )