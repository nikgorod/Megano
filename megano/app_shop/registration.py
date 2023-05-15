from django.contrib.auth import authenticate, login
from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.db import transaction
from django.shortcuts import redirect, render

from app_shop.models import UserProfile

from .forms import UserFormPassword, UserFormRegister


class ShopLoginView(LoginView):
    """Представление для аутентификации пользователя."""

    template_name = 'app_shop/register/login.html'

    def form_valid(self, form):
        response = super(ShopLoginView, self).form_valid(form)
        return response


class ShopLogoutView(LogoutView):

    template_name = 'app_shop/logout.html'
    next_page = '../main_page/'


class ShopPasswordReset(PasswordResetView):
    template_name = 'app_shop/register/password_reset_form.html'


class ShopPasswordResetDone(PasswordResetDoneView):
    template_name = 'app_shop/register/password_reset_done.html'


class ShopPasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'app_shop/register/password_reset_confirm.html'


class ShopPasswordResetComplete(PasswordResetCompleteView):
    template_name = 'app_shop/register/password_reset_complete.html'


def register_view(request):
    if request.method == "POST":
        user_form = UserFormRegister(request.POST)
        user_form_password = UserFormPassword(request.POST)
        if user_form.is_valid() and user_form_password.is_valid():
            with transaction.atomic():
                user = user_form_password.save()
                UserProfile.objects.create(
                    user=user,
                    first_name=user_form.cleaned_data.get('first_name'),
                    last_name=user_form.cleaned_data.get('last_name'),
                    middle_name=user_form.cleaned_data.get('middle_name'),
                    tel=user_form.cleaned_data.get('tel'),
                )
                email = user_form_password.cleaned_data.get('email')
                raw_password = user_form_password.cleaned_data.get('password1')
                auth_user = authenticate(email=email, password=raw_password)
                login(request, auth_user)
                return redirect('../main_page/')

    else:
        user_form = UserFormRegister()
        user_form_password = UserFormPassword()
    return render(request, 'app_shop/register/register.html', {'user_form': user_form,
                                                               'user_form_password': user_form_password})
