from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.urls import reverse

from .models import User
# Create your views here.
from django.contrib.auth import login
from django.views import View
import re
# 注册
def index(request):
    return HttpResponse("ok")
class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')
    def post(self,request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        mobile = request.POST.get("mobile")
        if not all([username, password, password2, mobile],):
            return HttpResponse("信息不完整")
        if not re.match(r'^[0-9a-zA-Z-_]{5,20}$', username):
            return HttpResponse("用户名有误")
        if not re.match(r'^[0-9a-zA-Z-_]{8,20}$', password):
            return HttpResponse("密码格式错误")

        if not password2 == password:
            return HttpResponse("密码错误")
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return HttpResponse("手机号输入有误")

        user = User.objects.create_user(username=username, password=password, mobile=mobile)

        request.session["username"] = user.username
        request.session["id"] = user.id
        login(request,user)
        response = redirect(reverse("concents:index"))
        response.set_cookie("username", user.username, max_age=1230)
        return response
class UsernameCountView(View):
    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        print("a")
        return JsonResponse({"count": count})
class MobileView(View):
    def get(self, request, mobile):
        count = User.objects.filter(mobile=mobile).count()


        return JsonResponse({"count": count})