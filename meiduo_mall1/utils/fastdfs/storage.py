# 自定义文件存储类

from django.core.files.storage import Storage

from django.conf import settings
class MyStorage(Storage):
    def _open(self, name, mode='rb'):
        pass
    def url(self, name):
        return "http://192.168.136.133:8888" + name
