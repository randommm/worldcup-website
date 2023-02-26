from django.urls import re_path

from . import views

app_name = "accounts"
urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^profile/', views.profile, name='profile'),
    re_path(r'^login/', views.login, name='login'),
    re_path(r'^logout/$', views.logout_view, name='logout'),
    re_path(r'^rpass/$', views.rpass, name='rpass'),
    re_path(r'^lemails/$', views.lemails, name='lemails'),
    re_path(r'^register_by_access_token/(?P<backend>[\w-]+)$', views.register_by_access_token,
        name='register_by_access_token'),
]
