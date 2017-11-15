from django.conf.urls import url

from . import views

app_name = "games"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^scoreboard$', views.scoreboard, name='scoreboard'),
    url(r'^games$', views.games, name='games'),
    url(r'^forecasts$', views.forecasts, name='forecasts'),
    url(r'^update_bet$', views.update_bet, name='update_bet'),
]
