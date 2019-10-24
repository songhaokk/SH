from django.conf.urls import url
from . import views
urlpatterns = [

    url(r'^index/$', views.index.as_view(), name="index"),
    url(r'^$', views.IndexView.as_view(), name="indexview"),

]

