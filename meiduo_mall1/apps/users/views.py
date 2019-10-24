import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.urls import reverse

from apps.users.utils import check_token
from celery_tasks.email.tasks import send_active_email
from utils.response_code import RETCODE
from .models import User
# Create your views here.
from django.contrib.auth import login
from django.views import View
import re

def index(request):
    return HttpResponse("ok")
# 注册
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
# 用户名重复
class UsernameCountView(View):
    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        print("a")
        return JsonResponse({"count": count})
# 手机号重复
class MobileView(View):
    def get(self, request, mobile):
        count = User.objects.filter(mobile=mobile).count()


        return JsonResponse({"count": count})
# 用户中心添加邮箱
class Email(LoginRequiredMixin,View):

    def put(self,request):
        body = request.body.decode()
        data = json.loads(body)
        email = data.get('email')
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return JsonResponse({"code":RETCODE.PARAMERR, "errmsg": "邮箱格式不对"})
        request.user.email = email
        request.user.save()


        send_active_email.delay(request.user.id, email)

        return JsonResponse({"code": RETCODE.OK, "errmsg": "ok"})

# 邮箱激活网址
class Semail(View):
    def get(self,request):
        token = request.get("token")
        if token is None:
            return HttpResponseBadRequest("缺少参数")

        id, email = check_token(token)
        if id and email is None:
            return HttpResponseBadRequest("验证失败")
        try:
            user = User.objects.get(id=id, email=email)
        except User.DoesNotExist:
            return HttpResponseBadRequest("验证失败")
        user.email_active = True
        user.save()
        return redirect(reverse("login:userinfo"))


        return HttpResponse("激活成功")


class AddressView(LoginRequiredMixin, View):
    """用户收货地址"""

    def get(self, request):
        """提供收货地址界面"""
        return render(request, 'user_center_site.html')

# 新增收货地址
from .models import Address
class CreateAddressView(LoginRequiredMixin, View):
    def post(self, request):
        count = Address.objects.filter(user=request.user).count()
        if count > 20:
            return HttpResponseBadRequest("地址已满")
        data = request.body.decode()
        data = json.loads(data)



#         收货人
        title = data.get("title")
        receiver = data.get("receiver")
        province = data.get("province")
        city = data.get("city")
        district = data.get("district")
        place = data.get("place")
        mobile = data.get("mobile")
        tel = data.get("tel")
        email = data.get("email")
        if not all([title, ]):
            return HttpResponseBadRequest("")


















