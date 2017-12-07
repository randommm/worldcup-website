from django.conf.urls import url

from . import views

app_name = "games"
urlpatterns = [
    url(r'^games$', views.games, name='games'),
    url(r'^scoreboard$', views.scoreboard, name='scoreboard'),
    url(r'^results$', views.results, name='results'),

    url(r'^update_bet$', views.update_bet, name='update_bet'),

    url(r'^forecasts$', views.forecasts, name='forecasts'),
    url(r'^rules$', views.rules, name='rules'),
    url(r'^history$', views.history, name='history'),
    url(r'^objectives$', views.objectives, name='objectives'),
    url(r'^contact$', views.contact, name='contact'),
]
