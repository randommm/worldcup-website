from django.urls import re_path

from . import views

app_name = "games"
urlpatterns = [
    re_path(r'^games/$', views.games, name='games'),
    re_path(r'^scoreboard/$', views.scoreboard, name='scoreboard'),
    re_path(r'^results/$', views.results, name='results'),

    re_path(r'^update_bet/$', views.update_bet, name='update_bet'),


    re_path(r'^leagues/$', views.league, name='league'),
    re_path(r'^leagues/create$', views.league_create, name='league_create'),
    re_path(r'^leagues/leave$', views.league_leave, name='league_leave'),
    re_path(r'^leagues/remove_user$', views.league_remove_user,
        name='league_remove_user'),

    re_path(r'^leagues/add_moderator$', views.league_add_moderator,
        name='league_add_moderator'),
    re_path(r'^leagues/remove_moderator$', views.league_remove_moderator,
        name='league_remove_moderator'),
    re_path(r'^leagues/transfer_admin$', views.league_transfer_admin,
        name='league_transfer_admin'),

    re_path(r'^leagues/ask_join$', views.league_ask_join,
        name='league_ask_join'),
    re_path(r'^leagues/add_user$', views.league_add_user,
        name='league_add_user'),


    re_path(r'^forecasts/$', views.forecasts, name='forecasts'),
    re_path(r'^rules/$', views.rules, name='rules'),
    re_path(r'^history/$', views.history, name='history'),
    re_path(r'^objectives/$', views.objectives, name='objectives'),
    re_path(r'^contact/$', views.contact, name='contact'),
    re_path(r'^terms/$', views.terms, name='terms'),

    re_path(r'^recreate/$', views.recreate, name='recreate'),
]
