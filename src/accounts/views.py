from django.shortcuts import render_to_response, redirect
from django.contrib.auth import (authenticate,
                                 get_user_model,
                                 login,
                                 logout,
                                 )
from .forms import UserLoginForm, UserRegisterForm
from django.template.context_processors import csrf

# Create your views here.


def login_view(request):
    form = UserLoginForm(request.POST or None)
    context = {}
    context.update(csrf(request))
    context['form'] = form
    context['inset'] = 'Login'
    next = request.GET.get('next')
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/')
    return render_to_response('form.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')


def register_view(request):
    form = UserRegisterForm(request.POST or None)
    context = {}
    context.update(csrf(request))
    context['form'] = form
    context['inset'] = 'Register'
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        return redirect('/')
    return render_to_response('form.html', context)
