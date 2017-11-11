from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import User, Team, Game, Bet, Predict, Result

from django import template

register = template.Library()

@register.filter(name='times')
def get_dict(dict_, key):
    if key in dict_:
        return dict_[key]

def index(request):
    return render(request, 'index.html')

def predictions(request):
    return HttpResponse("predictions")

def games(request):
    games = Game.objects#.order_by('-date')[:5]
    filter_by = list(games.values_list("id", flat=True))
    predictions = Predict.objects.filter(game_id__in=filter_by)

    games =

    games = [
             "team1":
             "team2":
             "predict":
             "prob1":
             "prob2":
            ]

    context = {'games': games, 'predictions': predictions}
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
