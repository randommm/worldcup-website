from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import User, Team, Game, Bet, Forecast, Result

def index(request):
    return render(request, 'index.html')

def forecasts(request):
    return HttpResponse("forecasts")

def games(request):
    games = (Game.objects.select_related("forecast")
                 .prefetch_related('bet_set')
                 .order_by('-date'))

    for game in games:
        try:
            game.forecast
            game.forecast.prob_tie = 100 - game.forecast.prob1 - game.forecast.prob2
        except (KeyError, Forecast.DoesNotExist):
            pass

        try:
            game.bet = game.bet_set.get(user_id=1)
            game.bet.prob_tie = 100 - game.bet.prob1 - game.bet.prob2
        except (KeyError, Bet.DoesNotExist):
            pass

    context = {'games': games}
    return render(request, 'games.html', context)

def scoreboard(request):
    return HttpResponse("scoreboard")

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'detail.html', {'question': question})
