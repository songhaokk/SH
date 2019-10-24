import json
import logging
logger = logging.getLogger('django')


from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.urls import reverse

from apps.users.utils import check_token
from celery_tasks.email.tasks import send_active_email
from utils.response_code import RETCODE
from .models import User, Address
# Create your views here.
from django.contrib.auth import login, logout
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


# class AddressView(LoginRequiredMixin, View):
#     """用户收货地址"""
#
#     def get(self, request):
#         """提供收货地址界面"""
#         return render(request, 'user_center_site.html')

# # 新增收货地址
from .models import Address
# class CreateAddressView(LoginRequiredMixin, View):
#     def post(self, request):
#         count = Address.objects.filter(user=request.user).count()
#         if count > 20:
#             return HttpResponseBadRequest("地址已满")
#         data = request.body.decode()
#         data = json.loads(data)
#
#
#
# #         收货人
#         title = data.get("title")
#         receiver = data.get("receiver")
#         province = data.get("province")
#         city = data.get("city")
#         district = data.get("district")
#         place = data.get("place")
#         mobile = data.get("mobile")
#         tel = data.get("tel")
#         email = data.get("email")
#         if not all([title, ]):
#             return HttpResponseBadRequest("")

class UserCenterSiteView(View):

    def get(self,request):

        user=request.user
        addresses = Address.objects.filter(user=user, is_deleted=False)

        address_dict_list = []
        for address in addresses:
            address_dict = {
                "id": address.id,
                "title": address.title,
                "receiver": address.receiver,
                "province": address.province.name,
                "province_id":address.province_id,
                "city": address.city.name,
                "city_id":address.city_id,
                "district": address.district.name,
                "district_id":address.district_id,
                "place": address.place,
                "mobile": address.mobile,
                "tel": address.tel,
                "email": address.email
            }
            address_dict_list.append(address_dict)


        context = {
            'default_address_id':user.default_address_id,
            'addresses':address_dict_list
        }
        return render(request,'user_center_site.html',context=context)

class CreateView(View):

    def post(self,request):

        count = Address.objects.filter(user=request.user,is_deleted=False).count()
        if count >= 20:
            return JsonResponse({'code': RETCODE.THROTTLINGERR, 'errmsg': '超过地址数量上限'})
        data = json.loads(request.body.decode())
        receiver=data.get('receiver')
        province_id=data.get('province_id')
        city_id=data.get('city_id')
        district_id=data.get('district_id')
        place=data.get('place')
        mobile=data.get('mobile')
        tel=data.get('tel')
        email=data.get('email')

        if not all([receiver,province_id,city_id,district_id,place,mobile]):

            return HttpResponseBadRequest('参数不全')
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return HttpResponseBadRequest('电话号码输入有误')
        if tel:
            if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
                return HttpResponseBadRequest('参数tel有误')
        if email:
            if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return HttpResponseBadRequest('参数email有误')
        try:
            ads = Address.objects.create(user=request.user,
                    title=receiver,
                    receiver=receiver,
                    province_id=province_id,
                    city_id=city_id,
                    district_id=district_id,
                    place=place,
                    mobile=mobile,
                    tel=tel,
                    email=email)
        except Exception as e:
            logger.error(e)
            return HttpResponseBadRequest('保存失败')

        address = {

            "receiver": ads.receiver,
            "province": ads.province.name,
            "city": ads.city.name,
            "district": ads.district.name,
            "place": ads.place,
            "mobile": ads.mobile,
            "tel": ads.tel,
            "email": ads.email,
            "id": ads.id,
            "title": ads.title,
        }

        return JsonResponse({'code': RETCODE.OK, 'errmsg': '新增地址成功', 'address': address})
class DefaultView(View):

    def put(self,request,address_id):

        try:
            default_address = Address.objects.get(id=address_id)
            request.user.default_address = default_address
            request.user.save()
        except Exception as e:
            logger.error(e)
            return HttpResponseBadRequest('出错')
        return JsonResponse({'code':RETCODE.OK,'errmsg': '设置成功'})

class UpdateView(View):

    def put(self,request,address_id):

        data = json.loads(request.body.decode())
        receiver=data.get('receiver')
        province_id=data.get('province_id')
        city_id=data.get('city_id')
        district_id=data.get('district_id')
        place=data.get('place')
        mobile=data.get('mobile')
        tel=data.get('tel')
        email=data.get('email')
        if not all([receiver,province_id,city_id,district_id,place,mobile]):

            return HttpResponseBadRequest('参数不全')
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return HttpResponseBadRequest('电话号码输入有误')
        if tel:
            if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
                return HttpResponseBadRequest('参数tel有误')
        if email:
            if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return HttpResponseBadRequest('参数email有误')

        try:
            update_address = Address.objects.filter(id=address_id)
            update_address.update(
                user=request.user,
                title=receiver,
                receiver=receiver,
                province_id=province_id,
                city_id=city_id,
                district_id=district_id,
                place=place,
                mobile=mobile,
                tel=tel,
                email=email,
            )
        except Exception as e:
            logger.error(e)
            return HttpResponseBadRequest('更新失败')
        update_address = Address.objects.get(id=address_id)
        address_dict = {
            "id": update_address.id,
            "title": update_address.title,
            "receiver": update_address.receiver,
            "province": update_address.province.name,
            "city": update_address.city.name,
            "district": update_address.district.name,
            "place": update_address.place,
            "mobile": update_address.mobile,
            "tel": update_address.tel,
            "email": update_address.email
        }

        return JsonResponse({'code': RETCODE.OK, 'errmsg': '更新地址成功', 'address': address_dict})
    def delete(self,request,address_id):

        try:
            delete_address = Address.objects.filter(id=address_id)
            delete_address.update(is_deleted=True)
        except Exception as e:
            logger.error(e)
            return HttpResponseBadRequest('删除失败')
        return JsonResponse({'code': RETCODE.OK, 'errmsg': '删除地址成功'})

class UpdateTitleView(View):

    def put(self,request,address_id):

        data = json.loads(request.body.decode())
        title = data.get('title')
        try:
            update_title_address = Address.objects.filter(id=address_id)
            update_title_address.update(title=title)
        except Exception as e:
            logger.error(e)
            return HttpResponseBadRequest('修改标题失败')
        return JsonResponse({'code': RETCODE.OK, 'errmsg': '设置地址标题成功'})
class ChangePassword(View):

    def get(self,request):

        return render(request,'user_center_pass.html')

    def post(self, request):
        """实现修改密码逻辑"""
        # 1.接收参数
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        new_password2 = request.POST.get('new_password2')
        # 2.验证参数
        if not all([old_password, new_password, new_password2]):
            return HttpResponseBadRequest('缺少必传参数')
        if not re.match(r'^[0-9A-Za-z]{8,20}$', new_password):
            return HttpResponseBadRequest('密码最少8位，最长20位')
        if new_password != new_password2:
            return HttpResponseBadRequest('两次输入的密码不一致')

        # 3.检验旧密码是否正确
        if not request.user.check_password(old_password):
            return render(request, 'user_center_pass.html', {'origin_password_errmsg': '原始密码错误'})
        # 4.更新新密码
        try:
            request.user.set_password(new_password)
            request.user.save()
        except Exception as e:
            logger.error(e)
            return render(request, 'user_center_pass.html', {'change_password_errmsg': '修改密码失败'})
        # 5.退出登陆,删除登陆信息
        logout(request)
        # 6.跳转到登陆页面
        response = redirect(reverse('users:login'))

        response.delete_cookie('username')

        return response

















