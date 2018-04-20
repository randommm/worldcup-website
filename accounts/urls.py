from django.conf.urls import url

from . import views

app_name = "accounts"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^rpass/$', views.rpass, name='rpass'),
    url(r'^lemails/$', views.lemails, name='lemails'),
]
