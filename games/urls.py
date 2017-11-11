from django.conf.urls import url

from . import views

app_name = "games"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^scoreboard$', views.scoreboard, name='scoreboard'),
    url(r'^games$', views.games, name='games'),
    url(r'^predictions$', views.predictions, name='predictions'),
]
