from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from .models import User, Team, Game, Bet, Forecast, Result


def index(request):
    return render(request, 'index.html')

def forecasts(request):
    return HttpResponse("forecasts")

def games(request):
    games = Game.objects.select_related("forecast").all()#.order_by('-date')[:5]

    for game in games:
        try:
            game.bet = game.bet_set.get(id=1)
            game.bet.prob_tie = 100 - game.bet.prob1 - game.bet.prob2
        except ObjectDoesNotExist:
            game.bet = None

        try:
            game.forecast
            game.forecast.prob_tie = 100 - game.forecast.prob1 - game.forecast.prob2
        except ObjectDoesNotExist:
            pass

    filter_by = list(games.values_list("id", flat=True))
    forecast = Forecast.objects.filter(game_id__in=filter_by)

    context = {'games': games}
    return render(request, 'games.html', context)

def scoreboard(request):
    return HttpResponse("scoreboard")



def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
