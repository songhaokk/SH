from collections import OrderedDict

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views import View

from apps.concents.models import ContentCategory
from apps.concents.utils import get_categories
from apps.goods.models import GoodsChannel


class index(View):
    def get(self, request):
        return render(request, "index.html")

# # fdfs上传文件的配制
# # 导入Fdfs包
# from  fdfs_client.client import Fdfs_client
# # 创建Fdfs客户端实例
# client=Fdfs_client("utils/fastdfs/client.conf")
# # 上传文件
# client.upload_by_filename("")
# # 获取上传数据




class IndexView(View):
    """首页广告"""

    def get(self, request):
        """提供首页广告界面"""
        # 查询商品频道和分类
        categories = get_categories()

        # 广告数据
        contents = {}
        content_categories = ContentCategory.objects.all()
        for cat in content_categories:
            contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')

        # 渲染模板的上下文
        context = {
            'categories': categories,
            'contents': contents,
        }
        return render(request, 'index.html', context)