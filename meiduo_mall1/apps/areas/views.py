from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
from django.views import View

from apps.areas.models import Area
from django.core.cache import cache

class AreasView(View):
    def get(self, request):
        id = request.GET.get("area_id")
        if id is None:
            # che = cache.get()  查询redis
            sheng = Area.objects.filter(parent=None)
            list_sheng = []
            for i in sheng:
                list_sheng.append(
                    {"id": i.id,
                     "name": i.name},

                    )
                # cache.set() 添加数据库
            return JsonResponse({"code":0, "province_list": list_sheng})

        else:
            # sheng = Area.objects.get(id=id)
            # shi = sheng.subs.all()
            shi = Area.objects.filter(parent_id=id)
            list_shi = []
            for i in shi:
                list_shi.append({
                    "id":i.id,
                    "name":i.name
                })
            return JsonResponse({"code":0, "subs":list_shi})



