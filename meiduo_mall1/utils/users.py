# 多用户登录
from django.contrib.auth.backends import ModelBackend
import re
from apps.login.views import loogin
from apps.users.models import User
def getmobie(request):
    try:
        if re.match(r'1[3-9]\d{9}', request):
            user = User.objects.get(mobile=request)
        else:
            user = User.objects.get(username=request)
    except Exception as e:
        return e
    else:
        return user

class Username(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = getmobie(username)
        if user and user.check_password(password):
            return user


