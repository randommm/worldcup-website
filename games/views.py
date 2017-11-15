from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import User, Team, Game, Bet, Forecast, Result
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'games/index.html')

def forecasts(request):
    return HttpResponse("Our forecasts will be here")
    #return HttpResponse(str(request.__dict__))

@login_required
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
            game.bet = game.bet_set.get(user_id=request.user.id)
            game.bet.prob_tie = 100 - game.bet.prob1 - game.bet.prob2
        except (KeyError, Bet.DoesNotExist):
            pass

    context = {'games': games}
    return render(request, 'games/games.html', context)

def update_bet(request):
    prob1 = request.POST.get("prob1")
    prob2 = request.POST.get("prob2")
    gameid = request.POST.get("gameid")

    bet = Bet.objects.update_or_create(
      user_id=request.user.id, game_id=gameid,
      defaults={'prob1': prob1, 'prob2': prob2}
    )
    #bet.save()

    return HttpResponse("sucess")

def scoreboard(request):
    return HttpResponse("The scoreboard will be here")

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'games/detail.html', {'question': question})
