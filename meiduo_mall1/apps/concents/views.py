from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views import View


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