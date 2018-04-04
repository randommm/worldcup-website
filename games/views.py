from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse
from .models import User, Team, Game, Bet, Result, Point, League
from .models import LeagueUser
from django.contrib.auth.decorators import login_required
from django.db import transaction, DatabaseError
from django.utils.timezone import get_current_timezone
import datetime
from .leagues import *
from django.utils.translation import get_language


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
    points_by_league = {}
    for result in results:
        bets = Bet.objects.filter(game_id = result.game_id)
        for bet in bets:
            prob_tie = 100 - bet.prob0 - bet.prob1
            if result.result == 0:
                bet.points = round(100 - (bet.prob1**2 + prob_tie**2 + bet.prob1 * prob_tie) / 100)
            elif result.result == 1:
                bet.points = round(100 - (bet.prob0**2 + prob_tie**2 + bet.prob0 * prob_tie) / 100)
            else:
                bet.points = round(100 - (bet.prob1**2 + bet.prob0**2 + bet.prob1 * bet.prob0) / 100)
            bet.save()
            user_id = bet.user_id
            if user_id not in points_by_user:
                points_by_user[user_id] = 0
            points_by_user[user_id] += bet.points

        result.committed = True
        result.save()

    for user_id, points in points_by_user.items():
        points_of_the_user = Point.objects.get_or_create(user_id=user_id)[0]
        points_of_the_user.points += points
        points_of_the_user.save()

        #Check if user has a league, if positive, adds his points to
        #points_by_league
        try:
            league_user = LeagueUser.objects.get(user_id=user_id)
            league_id = league_user.league_id
            if league_id not in points_by_league:
                points_by_league[league_id] = 0
            points_by_league[league_id] += points
        except (KeyError, LeagueUser.DoesNotExist):
            context = dict(must_have_league=True)

    for league_id, points in points_by_league.items():
        points_of_the_league = League.objects.get_or_create(id=league_id)[0]
        points_of_the_league.points += points
        points_of_the_league.save()

@transaction.atomic
def recreate(request):
    if (not request.user.is_authenticated or
        request.user.email not in ["m@marcoinacio.com",
                                   "marcoigarapava@gmail.com",
                                   "marcio.alves.diniz@gmail.com"]):
        raise Http404("")
    with transaction.atomic():
        Point.objects.all().delete()
        Bet.objects.all().update(points=-1)
        League.objects.all().update(points=0)
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

def terms(request):
    return render(request, 'games/terms.html')

def games(request):
    cutdate = datetime.datetime.now().timestamp()
    cutdate += 60*30
    cutdate = datetime.datetime.fromtimestamp(cutdate)
    games = (Game.objects
                 .select_related("team0")
                 .select_related("team1")
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

    if get_language() == "pt-br" or get_language() == "pt":
        for game in games:
            game.team0.name = game.team0.name_pt
            game.team1.name = game.team1.name_pt

    user_tz = get_current_timezone()

    context = {'games': games, 'user_tz': user_tz}
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

    return HttpResponse("success")

def scoreboard(request):
    committer()
    points = Point.objects.all().order_by('-points')

    context = {'points': points}
    return render(request, 'games/scoreboard.html', context)

def results(request):
    committer()
    bets = (Bet.objects.select_related("game")
            .filter(user=request.user.id))
    for bet in bets:
        if bet.points == -1:
            bet.pontuated = False
        else:
            bet.pontuated = True
        bet.ptie = 100 - bet.prob1 - bet.prob0

        if get_language() == "pt-br" or get_language() == "pt":
            bet.game.team0.name = bet.game.team0.name_pt
            bet.game.team1.name = bet.game.team1.name_pt

        if get_language() == "pt-br" or get_language() == "pt":
            victory = " venceu"
            draw = "empate"
        else:
            victory = " won"
            draw = "draw"

        try:
            result_code = bet.game.result.result
            if result_code == 0:
                bet.game.resultn = bet.game.team0.name + victory
            elif result_code == 1:
                bet.game.resultn = bet.game.team1.name + victory
            elif result_code == 2:
                bet.game.resultn = draw
        except (KeyError, Result.DoesNotExist):
            bet.game.resultn = None

    context = {'bets': bets}
    return render(request, 'games/results.html', context)
