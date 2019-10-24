import re
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, HttpResponse
# Create your views here.
from django.urls import reverse
from django.views import View

from apps.users.models import User
from meiduo_mall1 import settings
from .models import OAuthQQUser

#  QQ登陆
class QQlogin(View):
    def get(self, request):
        code = request.GET.get("code")
        state = request.GET.get("state")
        if code is None:
            return HttpResponseBadRequest("meiyou1code")
        # 导入QQ互联包
        from QQLoginTool.QQtool import OAuthQQ
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI,
                        state=state)
        # 获取token
        token = oauth.get_access_token(code)
        # 获取openid
        openid = oauth.get_open_id(token)
        # 判断openid
        try:
            qquser = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            return render(request, "oauth_callback.html", context={"openid":openid})
        else:
                login(request, qquser.user)


                response = redirect(reverse("concents:index"))
                response.set_cookie("username", qquser.user, max_age=3600*24)
                return response
        # return render(request, "oauth_callback.html")
    # QQ绑定
    def post(self, request):

        password = request.POST.get("pwd")
        mobile = request.POST.get("mobile")
        msg_code = request.POST.get("sms_code")
        openid = request.POST.get("openid")
        if not all([password, mobile, msg_code]):
            return HttpResponseBadRequest("budui")
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return HttpResponse("手机号输入有误")
        if not re.match(r'^[0-9a-zA-Z-_]{8,20}$', password):
            return HttpResponse("密码格式错误")

        from django.contrib.auth import authenticate
        user = authenticate(username=mobile, password=password, mobile=mobile, msg_code=msg_code)
        if user is None:
            return HttpResponseBadRequest("budui")
        if openid is None:
            return HttpResponseBadRequest("buzai")
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            user = User.objects.create_user(username=mobile, password=password, mobile=mobile)
        else:
            if not user.check_password(password):
                return HttpResponseBadRequest("bucunzai")
        OAuthQQUser.objects.create(user=user, openid=openid)


        login(request, user)
        response = redirect(reverse("concents:index"))
        response.set_cookie("username", user.username,max_age=1000)
        return response




