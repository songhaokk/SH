from django.conf.urls import url

from . import views
urlpatterns = [
    url(r'^index/', views.index),
    url(r'^index1/', views.register.as_view())

]
