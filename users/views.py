from django.contrib.auth.views import LoginView, PasswordResetConfirmView
from allauth.account.views import (
    PasswordChangeView,
    PasswordResetView)
from users.forms import *
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    UpdateView,
    TemplateView)
from django.contrib import messages
from users.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse


# Система регистрации
class RegistrationView(CreateView):
    template_name = 'users/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        messages.success(self.request,'You have registered successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


# Система авторизации
class AuthView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm

    def form_valid(self, form):
        messages.success(self.request,'You have logged successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        messages.error(self.request,'Wrong data, please try again!')
        return super().form_invalid(form)


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('index')

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class UserPassChangeView(PasswordChangeView):
    template_name = 'users/password_change.html'
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('index')


class UserPassResetView(PasswordResetView):
    template_name = 'users/password_reset.html'
    form_class = UserPassResetForm
    success_url = reverse_lazy('index')
    email_template_name = 'users/password_reset_email.html'

    def post(self, request, *args, **kwargs):
        current_site = get_current_site(request)
        reset_password_url = reverse_lazy('password_reset')
        reset_url = request.build_absolute_uri(reset_password_url + '/')

        send_mail(
            'reset password',
            f' link for reset: {reset_url}',
            'root@site.com',
            ['you@mail.com'],
            fail_silently=False,
        )
        return HttpResponse('its ok')

    def form_valid(self, form):
        messages.success(self.request, 'Instruction have sent to your email, please check!')
        return super().form_valid(form)


class UserPassResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('login_pg')

    def form_valid(self, form):
        messages.success(self.request, 'Your password have reseted successfully')
        return super().form_valid(form)