from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, HttpResponse
# Create your views here.
from django.urls import reverse
from django.views import View
import re
# 多账号登陆
class loogin(View):
    def get(self, request):
        return render(request, "login.html")
    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("pwd")
        remembered = request.POST.get("remembered")
        if not all([username, password]):
            return HttpResponseBadRequest("信息不全")
        if not(re.match(r'^[a-zA-Z0-9_-]{5,20}$', "password")):
            return HttpResponseBadRequest("")
        if not(re.match(r'^[a-zA-Z0-9_-]{5,20}$', 'username')):
            return HttpResponseBadRequest("")
        from django.contrib.auth import authenticate
        # 认证登陆
        user = authenticate(username=username, password=password)
        if user is None:
            return HttpResponseBadRequest("账号或密码不正确")
        # 状态保持（已设置session）
        login(request, user)
        # 设置状态保持周期
        if remembered != "on":
            request.session.set_expiry(0)
        else:
            # 保持两周
            request.session.set_expiry(None)
        response = redirect(reverse("concents:index"))
        response.set_cookie("username", user.username, max_age=1230)
        return response


# 退出登陆
class logoutuser(View):
    def get(self, request):

        logout(request)

        response = redirect(reverse("login:login"))
        response.delete_cookie("username")
        return response
# 用户中心
# LoginRequiredMixin判断用户是否登录（）
# 搭配LoginRequiredMixin表示当用户未通过登录验证时，将用户重定向到登录页面。
# 在setting中设置   LOGIN_URL = '/login/'



from django.contrib.auth.mixins import LoginRequiredMixin
class UserInfo(LoginRequiredMixin, View):

    def get(self,request):
        return render(request, "user_center_info.html")

