#- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from rest_framework.authtoken.models import Token
from django import forms
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.utils.safestring import mark_safe
from app.models import UserProfile
import random
import json
import math

@csrf_exempt
def index(request):
    context = RequestContext(request)
    context_dict = {}
    return render_to_response('game/index.html', context_dict, context)

@csrf_exempt
def start_game(request):
    context = RequestContext(request)
    context_dict = {}
    if request.user.is_superuser:
        array = list(User.objects.all())
        array = array[1: len(array)]
        random.shuffle(array)
        for i in range(len(array) - 1):
            UserProfile.objects.get(user = array[i]).definition_killer(array[i + 1])
        UserProfile.objects.get(user = array[len(array) - 1]).definition_killer(array[0])
        context_dict = {'boldmessage': 'Success!'}
    else:
        context_dict = {'boldmessage': 'IDI NAHYI!'}
    return render_to_response('game/start_game.html', context_dict, context)

@csrf_exempt
def setLocation(request):
    if request.method == 'POST':
        result = request.body.decode("utf-8")
        a = json.loads(result)
        token = Token.objects.get(key = request.META['HTTP_TOKEN'])
        up = UserProfile.objects.get(user = token.user)
        up_killer = UserProfile.objects.get(user = UserProfile.objects.get(user = token.user).get_killer())
        up.set_x(a['lat'])
        up.set_y(a['lon'])
        def findKiller(user):
            array = list(User.objects.all())
            array = array[1: len(array)]
            for i in range(len(array)):
                if UserProfile.objects.get(user = array[i]).get_killer() == user:
                    return array[i]
            return user
        up_def = UserProfile.objects.get(user = findKiller(token.user))
        data = {'x_locate': up_killer.get_x(), 'y_locate': up_killer.get_y(), 'status': up_killer.get_status(), 'alive': up.get_alive(), 'x_killer': up_def.get_x(), 'y_killer': up_def.get_y()}
        return HttpResponse(json.dumps(data))
    else:
        return HttpResponse('200')

@csrf_exempt
def toKillUser(request):
    token = Token.objects.get(key = request.META['HTTP_TOKEN'])
    up = UserProfile.objects.get(user = token.user)
    up_killer = UserProfile.objects.get(user = UserProfile.objects.get(user = token.user).get_killer())
    def deg2rad(deg):
        return deg * (math.pi / 180.0)
    def getDistance(lat1, lon1, lat2, lon2):
        R = 6371.0
        dLat = deg2rad(lat2 - lat1)
        dLon = deg2rad(lon2 - lon1)
        a = math.sin(dLat / 2.0) * math.sin(dLat / 2.0) + math.cos(deg2rad(lat1)) * math.cos(deg2rad(lat2)) * math.sin(dLon / 2.0) * math.sin(dLon / 2.0)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = R * c * 1000
        return math.ceil(d)
    def status_game():
        arr = list(User.objects.all())
        arr = arr[1: len(arr)]
        k = 0
        for i in range(len(arr)):
            up = UserProfile.objects.get(user = arr[i])
            if up.get_alive() == '1':
                k += 1
            if k > 1:
                return False
        return True
    result = getDistance(float(up.get_x()), float(up.get_y()), float(up_killer.get_x()), float(up_killer.get_y()))
    if result <= 100 and up_killer.get_status() == '1':
        up.definition_killer(up_killer.get_killer())
        up_killer.set_alive('0')
        if status_game():
            return HttpResponse(json.dumps({'winner': 'WIN'}))
        else:
            return HttpResponse(json.dumps({'winner': 'WP'}))
    else:
        return HttpResponse(json.dumps({'winner': 'net'}))

        
@csrf_exempt
def take_numbers(request):
    token = Token.objects.get(key = request.META['HTTP_TOKEN'])
    up = UserProfile.objects.get(user = UserProfile.objects.get(user = token.user).get_killer())
    data = {'x_locate': up.get_x(), 'y_locate': up.get_y(), 'status': up.get_status()}
    return HttpResponse(json.dumps(data))

@csrf_exempt
def log(request):
    if request.method == 'POST':
        data = request.body.decode("utf-8")
        result = json.loads(data)
        a = result['login']
        b = result['password']
        user = authenticate(username=a, password=b)
        print(a)
        print(b)
        if user is not None:
            if user.is_active:
                login(request, user)
                Token.objects.get_or_create(user = user)
                up = UserProfile.objects.get(user = user)
                up.def_status('1')
                return HttpResponse(json.dumps({'token': user.auth_token.key}))
            else:
                return HttpResponse(json.dumps({'token': '-1'}))
        else:
            context_dict = {'token': '-1'}
            return HttpResponse(json.dumps(context_dict))
    else:
        return HttpResponse('800')

@csrf_exempt
def logout_view(request):
    if Token.objects.get(key = request.META['HTTP_TOKEN']).user is not None:
        up = UserProfile.objects.get(user = Token.objects.get(key = request.META['HTTP_TOKEN']).user)
        up.def_status('0')
        Token.objects.get(key = request.META['HTTP_TOKEN']).user.auth_token.delete()
        return HttpResponse(json.dumps({'token': '-1'}))
    else:
        return HttpResponse('800')

@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        if User.objects.filter(username = data['login']).exists() is False:
            user = User.objects.create_user(data['login'], data['email'], data['password'])
            user.is_active=True
            user.save()
            print(user)
            UserProfile.objects.create(user = user, killer = user)
            up = UserProfile.objects.get(user = user)
            up.definition_killer(user)
            Token.objects.get_or_create(user = user)
            return HttpResponse(json.dumps({'token': user.auth_token.key}))
        else:
            return HttpResponse(json.dumps({'token': 'Bad boy'}))
    else:
        return HttpResponse('800')
