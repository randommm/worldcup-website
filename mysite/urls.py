from django.urls import re_path, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from games.views import index

urlpatterns = [
    re_path(r'^$', index, name='index'),
    re_path(r'^games/', include('games.urls')),
    re_path(r'^accounts/', include('accounts.urls')),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^social-login/', include('social_django.urls', namespace='social')),
]

urlpatterns += staticfiles_urlpatterns()
