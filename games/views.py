from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import User, Team, Game, Bet, Forecast, Result
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'games/index.html')

def rules(request):
    return render(request, 'games/rules.html')

def  history(request):
    return render(request, 'games/history.html')

def  objectives(request):
    return render(request, 'games/objectives.html')

def  contact(request):
    return render(request, 'games/contact.html')

def forecasts(request):
    return render(request, 'games/forecasts.html')
    #return HttpResponse("Our forecasts will be here")
    #return HttpResponse(str(request.__dict__))

@login_required
def games(request):
    games = (Game.objects.select_related("forecast")
                 .prefetch_related('bet_set')
                 .order_by('-date'))

    for game in games:
        try:
            game.forecast
            game.forecast.prob_tie = 100 - game.forecast.prob0 - game.forecast.prob1
        except (KeyError, Forecast.DoesNotExist):
            pass

        try:
            game.bet = game.bet_set.get(user_id=request.user.id)
            game.bet.prob_tie = 100 - game.bet.prob0 - game.bet.prob1
        except (KeyError, Bet.DoesNotExist):
            pass

    context = {'games': games}
    return render(request, 'games/games.html', context)

def update_bet(request):
    prob0 = int(request.POST.get("prob0"))
    prob1 = int(request.POST.get("prob1"))
    gameid = request.POST.get("gameid")

    assert(prob0 >= 0)
    assert(prob1 >= 0)
    assert(prob0 + prob1 <= 100)

    bet = Bet.objects.update_or_create(
      user_id=request.user.id, game_id=gameid,
      defaults={'prob0': prob0, 'prob1': prob1}
    )
    #bet.save()

    return HttpResponse("sucess")

def scoreboard(request):
    return render(request, 'games/scoreboard.html')

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'games/detail.html', {'question': question})
