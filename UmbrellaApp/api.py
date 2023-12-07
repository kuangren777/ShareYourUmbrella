# -*- coding: utf-8 -*-
# @Time    : 2023/12/3 17:43
# @Author  : KuangRen777
# @File    : api.py.py
# @Tags    :
import datetime
import random

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, HttpResponse

from .filters import OrderFilter
from .forms import *

from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


def user_login(request):
    if request.method == 'POST':
        # 获取 POST 请求中的用户名和密码
        username = request.POST.get('name')
        password = request.POST.get('password')

        # 使用 Django 内置的 authenticate 函数来验证用户
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # 如果用户验证成功，则登录用户
            login(request, user)
            return JsonResponse({'token': user.username})
        else:
            # 如果用户验证失败，返回错误消息
            return JsonResponse({'msg': '用户名或密码错误'}, status=401)

    # 如果不是 POST 请求，返回错误消息
    return JsonResponse({'msg': '请求方法不支持'}, status=405)
