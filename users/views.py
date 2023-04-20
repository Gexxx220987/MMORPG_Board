from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .models import User
from .forms import SignUpForm, ConfirmationSignUpForm, CustomLoginForm


class SignUp(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'users/signup.html'

    def get_success_url(self):
        return reverse_lazy('users:signup_check_email',
                            kwargs={'pk': self.object.pk})


class SignUpCheckEmail(UpdateView):
    model = User
    template_name = 'users/signup_check_email.html'
    form_class = ConfirmationSignUpForm
    success_url = reverse_lazy('users:login')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user_pk'] = self.kwargs['pk']
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        user.is_active = True
        user.save()
        return response


class UserLogin(LoginView):
    template_name = 'users/login.html'
    fields = ['username', 'password']
    form_class = CustomLoginForm

    def get_success_url(self):
        return reverse_lazy('board:index')


class UserLogout(LogoutView):
    next_page = reverse_lazy('users:login')
