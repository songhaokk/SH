from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^index/$', views.index),
    url(r'^register/$', views.RegisterView.as_view(), name="register"),
    url(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/$', views.UsernameCountView.as_view()),
    url(r'^mobile/(?P<mobile>1[3-9]\d{9})/$', views.MobileView.as_view()),
    url(r'^emails/', views.Email.as_view(), name="emails"),
    url(r'^semail/', views.Semail.as_view(), name="Semail"),
    # url(r'^add/', views.AddressView.as_view(), name="add"),
    url(r'^address/$', views.UserCenterSiteView.as_view(), name='address'),
    url(r'^addresses/create/$',views.CreateView.as_view(),name='createaddress'),
    url(r'^addresses/(?P<address_id>\d+)/default/$',views.DefaultView.as_view(),name='defaultaddress'),
    url(r'^addresses/(?P<address_id>\d+)/$',views.UpdateView.as_view(),name='updateaddress'),
    url(r'^addresses/(?P<address_id>\d+)/title/$',views.UpdateTitleView.as_view(),name='updateaddressTitle'),
    url(r'^changepwd/$', views.ChangePassword.as_view(), name='changepwd'),
]

