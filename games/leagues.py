from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.urls import reverse
from .models import User, Team, Game, Bet, Result, Point, League
from .models import LeagueUser, LeagueAsked
from django.contrib.auth.decorators import login_required
from django.db import transaction, DatabaseError
import re

max_league_members = 30

def league(request):
    from .views import committer
    committer()

    user_id = request.user.id

    if not request.user.is_authenticated:
        context = dict(must_signin=True)
    else:
        try:
            league_user = (LeagueUser.objects
                                     .select_related("league")
                                     .get(user_id=user_id))
            league = league_user.league

            users = (LeagueUser.objects
                               .select_related('user')
                               .filter(league_id=league.id))
            for user in users:
                user_auth = user.user
                user.first_name = user_auth.first_name
                user.last_name = user_auth.last_name
                try:
                    user.points = user_auth.point.points
                except (KeyError, Point.DoesNotExist):
                    user.points = 0

            users = sorted(users, key=lambda x: getattr(x, "points"),
                           reverse=True)


            if len(users) < max_league_members:
                users_invited = (LeagueAsked.objects
                                          .select_related('user')
                                          .filter(league_id=league.id))
            else:
                users_invited = None

            context = {'league_user': league_user,
                       'league': league,
                       'users': users,
                       'users_invited': users_invited}
        except (KeyError, LeagueUser.DoesNotExist):
            asked_leagues = LeagueAsked.objects.filter(user_id=user_id)
            available_leagues = League.objects.filter(user_count__lt=max_league_members)

            asked_leagues_ids = list()
            for aleague in asked_leagues:
               asked_leagues_ids.append(aleague.league_id)

            for league in available_leagues:
               if league.id in asked_leagues_ids:
                   league.asked = True
               else:
                   league.asked = False

            try:
                league_join = int(request.GET.get('league_join'))
                league_join = League.objects.get(id=league_join,
                                                 user_count__lt=max_league_members)
                if league_join.leagueasked_set.filter(user_id=user_id):
                    league_join = False
            except (TypeError, ValueError, League.DoesNotExist):
                league_join = False


            context = {'must_have_league': True,
                       'league_join': league_join,
                       'available_leagues': available_leagues}

    return render(request, 'games/league.html', context)



#CREATE LEAGUE FUNCTIONS
@login_required
@transaction.atomic
def league_create(request):
    league_name = request.POST.get("data")
    user_id = request.user.id

    #Replace sequential multiple space to a single one
    league_name = re.sub('\ +', ' ', league_name)

    #Strip initial white space (if any)
    league_name = re.sub('^\ ', '', league_name)

    if len(league_name) > 50 or len(league_name) < 5:
        return HttpResponseForbidden("invalid_league_name_length")

    #First letter to uppercase
    league_name = league_name[0].upper() + league_name[1:]

    if not league_name or not re.fullmatch('^[\w\ ]+$', league_name):
        return HttpResponseForbidden("invalid_league_name")

    league_user = LeagueUser.objects.filter(user_id=user_id)
    if league_user.count() > 0:
        return HttpResponseForbidden("user_have_league")

    league_check = League.objects.filter(name=league_name)
    if league_check.count() > 0:
        return HttpResponseForbidden("name_taken")

    league = League.objects.create(name=league_name)
    LeagueUser.objects.create(league_id=league.id,
                              user_id=user_id,
                              admin=1, moderator=1)
    LeagueAsked.objects.filter(user_id=user_id).delete()
    return HttpResponse("success")







# LEAVE AND REMOVE FUNCTIONS
@login_required
@transaction.atomic
def league_leave(request):
    if request.POST.get("data") != "pass":
        return HttpResponseForbidden("must_use_post")

    league_user = (LeagueUser.objects.get(user_id=request.user.id))
    league = league_user.league

    if league_user.admin:
        if league.leagueuser_set.count() > 1:
            return HttpResponseForbidden("must_empty_or_transfer_group")
        else:
            league_user.delete()
            league.delete()
    else:
        league_user.delete()
        league.user_count -= 1
        league.save()

    return HttpResponse("success")

@login_required
@transaction.atomic
def league_remove_user(request):
    p_user_id = int(request.POST.get("data"))

    a_league_user = LeagueUser.objects.get(user_id=request.user.id)

    if not a_league_user.admin and not a_league_user.moderator:
        return HttpResponseForbidden("not_admin_nor_mod")

    if p_user_id == request.user.id:
        return HttpResponseForbidden("cannot_autoremove")

    p_league_user = LeagueUser.objects.get(user_id=p_user_id)

    #Check if moderator is trying to remove another moderator or admin
    if (not a_league_user.admin and
        (p_league_user.admin or
         p_league_user.moderator)):
        return HttpResponseForbidden("cannot_remove_adm_nor_mod")

    p_league_user.delete()

    league = a_league_user.league
    league.user_count -= 1
    league.save()

    return HttpResponse("success")



# MODERATOR ADD AND REMOVE FUNCTIONS
@login_required
@transaction.atomic
def league_transfer_admin(request):
    p_user_id = int(request.POST.get("data"))

    a_league_user = (LeagueUser.objects
                     .select_related("league")
                     .get(user_id=request.user.id))

    if not a_league_user.admin:
        if p_user_id != request.user.id or add: #allow auto-remove
             return HttpResponseForbidden("not_admin")

    new_adm = LeagueUser.objects.get(league=a_league_user.league,
                                     user_id=p_user_id)
    new_adm.admin = 1
    new_adm.moderator = 1
    new_adm.save()

    a_league_user.admin = 0
    a_league_user.moderator = 1
    a_league_user.save()

    return HttpResponse("success")


# MODERATOR ADD AND REMOVE FUNCTIONS
@login_required
@transaction.atomic
def league_add_or_remove_moderator(request, add):
    p_user_id = int(request.POST.get("data"))

    a_league_user = (LeagueUser.objects
                     .select_related("league")
                     .get(user_id=request.user.id))

    if not a_league_user.admin:
        if p_user_id != request.user.id or add: #allow auto-remove
             return HttpResponseForbidden("not_admin")

    mod = LeagueUser.objects.get(league=a_league_user.league,
                                 user_id=p_user_id)
    mod.moderator = add
    mod.save()
    return HttpResponse("success")

@login_required
@transaction.atomic
def league_add_moderator(request):
    return league_add_or_remove_moderator(request, 1)

@login_required
@transaction.atomic
def league_remove_moderator(request):
    return league_add_or_remove_moderator(request, 0)






#ADD USER AND ASK TO JOIN FUNCTIONS
@login_required
@transaction.atomic
def league_add_user(request):
    p_user_id = int(request.POST.get("data"))
    a_user_id = request.user.id

    a_league_user = (LeagueUser.objects.select_related("league")
                               .get(user_id=a_user_id))

    league_id = a_league_user.league.id

    if not a_league_user.admin and not a_league_user.moderator:
        return HttpResponseForbidden("not_admin_nor_mod")

    check_member = LeagueUser.objects.filter(user_id=p_user_id)
    if check_member.count() > 0:
        return HttpResponseForbidden("user_already_has_league")

    check_league = League.objects.filter(id=league_id)
    if check_league.count() >= max_league_members:
        return HttpResponseForbidden("league_full")

    check_asked = LeagueAsked.objects.filter(user_id=p_user_id,
                                             league_id=league_id)
    if not check_league.count():
        return HttpResponseForbidden("user_did_not_asked_to_join")

    LeagueAsked.objects.filter(user_id=p_user_id).delete()
    LeagueUser.objects.create(user_id=p_user_id, league_id=league_id)

    league = a_league_user.league
    league.user_count += 1
    league.save()

    return HttpResponse("success")

@login_required
@transaction.atomic
def league_ask_join(request):
    league_id = int(request.POST.get("data"))
    user_id=request.user.id

    check_member = LeagueUser.objects.filter(user_id=user_id)
    if check_member.count() > 0:
        return HttpResponseForbidden("user_already_has_league")

    check_league = League.objects.filter(id=league_id)
    if check_league.count() >= max_league_members:
        return HttpResponseForbidden("league_full")

    LeagueAsked.objects.update_or_create(user_id=user_id,
                                         league_id=league_id)

    return HttpResponse("success")
