from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^login/$', views.loogin.as_view(), name="login"),
    url(r'^logout/$', views.logoutuser.as_view(), name="logout"),
    url(r'^userinfo/$', views.UserInfo.as_view(), name="userinfo"),
]