from django.conf.urls import url

from . import views

app_name = "games"
urlpatterns = [
    url(r'^games/$', views.games, name='games'),
    url(r'^scoreboard/$', views.scoreboard, name='scoreboard'),
    url(r'^results/$', views.results, name='results'),

    url(r'^update_bet/$', views.update_bet, name='update_bet'),

    url(r'^league/$', views.league, name='league'),
    url(r'^league/create$', views.league_create, name='league_create'),
    url(r'^league/leave$', views.league_leave, name='league_leave'),
    url(r'^league/remove_user$', views.league_remove_user,
        name='league_remove_user'),
    url(r'^league/add_moderator$', views.league_add_moderator,
        name='league_add_moderator'),
    url(r'^league/remove_moderator$', views.league_remove_moderator,
        name='league_remove_moderator'),

    url(r'^forecasts/$', views.forecasts, name='forecasts'),
    url(r'^rules/$', views.rules, name='rules'),
    url(r'^history/$', views.history, name='history'),
    url(r'^objectives/$', views.objectives, name='objectives'),
    url(r'^contact/$', views.contact, name='contact'),

    url(r'^recreate/$', views.recreate, name='recreate'),
]
