
from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^oauth_callback', views.QQlogin.as_view(), name='qqlogin')

]