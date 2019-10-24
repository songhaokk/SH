from django.shortcuts import render

# Create your views here.


from django.views import View

from apps.goods.models import GoodsCategory

# 面包屑导航
class ListView(View):
    def get(self, request, category_id,page):
        try:
            category=GoodsCategory.object.get(id=category_id)
        except GoodsCategory.DoesNotExist:
            return render(request,"404.html")


