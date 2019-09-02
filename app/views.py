#- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.utils.safestring import mark_safe
import random
import json

@csrf_exempt
def index(request):
    context = RequestContext(request)
    context_dict = {}
    return render_to_response('game/index.html', context_dict, context)


@csrf_exempt
def take_numbers(request):
    a = random.randint(1, 6)
    b = random.randint(1, 6)
    data = {'length': a, 'height': b, 'success': True}
    print(data)
    return HttpResponse(json.dumps(data))

@csrf_exempt
def log(request):
    context = RequestContext(request)
    if request.method == 'POST':
        a = request.POST['login']
        b = request.POST['password']
        user = authenticate(username=a, password=b)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('../index')
            else:
                context_dict = {'boldmessage': "Данный аккаунт неактивен"}
                return render_to_response('game/login.html', context_dict, context)
        else:
            context_dict = {'boldmessage': "Неверный логин или пароль"}
            return render_to_response('game/login.html', context_dict, context)
    context_dict = {'boldmessage': ""}
    return render_to_response('game/login.html', context_dict, context)

@csrf_exempt
def logout_view(request):
    auth.logout(request)
    return render(request,'game/index.html')

@csrf_exempt
def register(request):
    if request.method == 'POST':
        a = request.POST['login']
        b = request.POST['password']
        c = request.POST['email']
        user = User.objects.create_user(a, c, b)
        user.is_active=True
        user.save()
        return redirect('../index')
    context = RequestContext(request)
    context_dict = {}
    return render_to_response('game/registration.html', context_dict, context)
