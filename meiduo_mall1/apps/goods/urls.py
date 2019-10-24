from django.conf.urls import url
from . import views
urlpatterns = [

    url(r'^areas/$', views.ListView.as_view(), name="aresa")
]