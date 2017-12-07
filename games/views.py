from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse
from .models import User, Team, Game, Bet, Result, Point
from django.contrib.auth.decorators import login_required
from django.db import transaction, DatabaseError
import datetime

@transaction.atomic
def committer():
    results = Result.objects.exclude(committed=True)
    if results.count() == 0:
        return

    try:
        results = (Result.objects
                   .select_for_update(nowait=True)
                   .exclude(committed=True))
    except DatabaseError:
        return

    points_by_user = {}
    for result in results:
        bets = Bet.objects.filter(game_id = result.game_id)
        for bet in bets:
            if result.result == 0:
                bet.points = (10000 - (100 - bet.prob0)**2)
            elif result.result == 1:
                bet.points = (10000 - (100 - bet.prob1)**2)
            else:
                bet.points = (10000 - (bet.prob0 + bet.prob1)**2)
            bet.save()
            id_ = bet.user_id
            if id_ not in points_by_user:
                points_by_user[id_] = 0
            points_by_user[id_] += bet.points

        result.committed = True
        result.save()

    for id_, points in points_by_user.items():
        points_of_the_user = Point.objects.get_or_create(user_id=id_)[0]
        points_of_the_user.points += points
        points_of_the_user.save()

@transaction.atomic
def recreate(request):
    if (not request.user.is_authenticated or
        request.user.email not in ["m@marcoinacio.com",
                                   "marcoigarapava@gmail.com"]):
        raise Http404("")
    with transaction.atomic():
        Point.objects.all().delete()
        Result.objects.all().update(committed=False)
    committer()
    return HttpResponse("recreated")

def index(request):
    return render(request, 'games/index.html')

def rules(request):
    return render(request, 'games/rules.html')

def history(request):
    return render(request, 'games/history.html')

def objectives(request):
    return render(request, 'games/objectives.html')

def contact(request):
    return render(request, 'games/contact.html')

def forecasts(request):
    return render(request, 'games/forecasts.html')
    #return HttpResponse("Our forecasts will be here")
    #return HttpResponse(str(request.__dict__))

def games(request):
    cutdate = datetime.datetime.now().timestamp()
    cutdate += 60*30
    cutdate = datetime.datetime.fromtimestamp(cutdate)
    games = (Game.objects#.select_related("forecast")
                 .prefetch_related('bet_set')
                 .filter(date__gte=cutdate)
                 .order_by('date'))

    for game in games:
        try:
            bet = game.bet_set.get(user_id=1)
            game.site_forecast = type('site_forecast', (object,), {})()
            game.site_forecast.prob0 = bet.prob0
            game.site_forecast.prob1 = bet.prob1
            game.site_forecast.prob_tie = 100 - bet.prob0 - bet.prob1
        except (KeyError, Bet.DoesNotExist):
            pass

        if request.user.is_authenticated:
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

    if (Game.objects.get(id=gameid).date.timestamp() -
        datetime.datetime.now().timestamp() -
        60*30 >= 0):
        bet = Bet.objects.update_or_create(
          user_id=request.user.id, game_id=gameid,
          defaults={'prob0': prob0, 'prob1': prob1}
        )
    #bet.save()

    return HttpResponse("sucess")

def scoreboard(request):
    committer()
    points = Point.objects.all().order_by('-points')

    for point in points:
       pointunf = point.points
       if pointunf <= 1000:
           point.pointf = str(pointunf) + " P"
       elif pointunf <= 1000000:
           point.pointf = str(pointunf / 1000) + " KP"
       else:
           point.pointf = str(pointunf / 1000000) + " MP"

    context = {'points': points}
    return render(request, 'games/scoreboard.html', context)

def results(request):
    committer()
    bets = (Bet.objects.select_related("user")
            .filter(user=request.user.id))
    for bet in bets:
       if bet.points == -1:
          bet.pontuated = False
       else:
          bet.pontuated = True
       bet.ptie = 100 - bet.prob1 - bet.prob0;

    context = {'bets': bets}
    return render(request, 'games/results.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'games/detail.html', {'question': question})
