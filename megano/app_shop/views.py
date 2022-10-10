from django.contrib.auth import authenticate, login
from django.db import transaction
from django.shortcuts import render, redirect
from django.views import View
from .models import GoodCategory, UserProfile, User
from .forms import UserFormRegister, UserFormPassword
from django.db import IntegrityError
from django.contrib import messages


class MainPage(View):

    def get(self, request):
        good_categories = GoodCategory.objects.filter(active_goods=True)

        return render(request, 'app_shop/index.html', {'good_categories': good_categories})


def register_view(request):
    if request.method == "POST":
        user_form = UserFormRegister(request.POST)
        user_form_password = UserFormPassword(request.POST)
        if user_form.is_valid() and user_form_password.is_valid():
            try:
                with transaction.atomic():
                    user = user_form_password.save()
                    user.email = user_form.cleaned_data.get('email')
                    user.save()
                    UserProfile.objects.create(
                        user=user,
                        first_name=user_form.cleaned_data.get('first_name'),
                        last_name=user_form.cleaned_data.get('last_name'),
                        middle_name=user_form.cleaned_data.get('middle_name'),
                        tel=user_form.cleaned_data.get('tel'),
                        email=user_form.cleaned_data.get('email')
                    )
                    email = user_form.cleaned_data.get('email')
                    raw_password = user_form_password.cleaned_data.get('password1')
                    auth_user = authenticate(email=email, password=raw_password)
                    login(request, auth_user)
                    return redirect('../main_page/')

            except IntegrityError:
                messages.add_message(request, messages.INFO, 'Пользователь с таким Email уже существует!')

    else:
        user_form = UserFormRegister()
        user_form_password = UserFormPassword()
    return render(request, 'app_shop/register.html', {'user_form': user_form, 'user_form_password': user_form_password})
