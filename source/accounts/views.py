from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from main.settings import HOST_NAME
from accounts.models import Token
from accounts.forms import UserCreationForm
from django.contrib.auth.models import User


def login_view(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('webapp:index')
        else:
            context['has_error'] = True
    return render(request, 'login.html', context=context)


def logout_view(request):
    logout(request)
    return redirect('webapp:index')


def register_view(request):
    if request.method == 'GET':
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form})
    elif request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                is_active=False  # user не активный до подтверждения email
            )
            user.set_password(form.cleaned_data['password'])
            user.save()

            # токен для активации, его сложнее угадать, чем pk user-а.
            token = Token.objects.create(user=user)
            activation_url = HOST_NAME + reverse('accounts:user_activate') + '?token={}'.format(token)

            # отправка письма на email пользователя
            user.email_user('Регистрация на сайте localhost',
                            'Для активации перейдите по ссылке: {}'.format(activation_url))

            return redirect("webapp:index")
        else:
            return render(request, 'register.html', {'form': form})


def user_activate(request):
    token_value = request.GET.get('token')
    try:
        # найти токен
        token = Token.objects.get(token=token_value)

        # активировать пользователя
        user = token.user
        user.is_active = True
        user.save()

        # удалить токен, он больше не нужен
        token.delete()

        # войти
        login(request, user)

        # редирект на главную
        return redirect('webapp:index')
    except Token.DoesNotExist:
        # если токена нет - сразу редирект
        return redirect('webapp:index')
