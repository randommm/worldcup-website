from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.urls import reverse
from .models import User, Team, Game, Bet, Result, Point, League
from .models import LeagueUser
from django.contrib.auth.decorators import login_required
from django.db import transaction, DatabaseError

def league(request):
    from .views import committer
    committer()

    if not request.user.is_authenticated:
        context = dict(must_signin=True)
    else:
        try:
            league_user = (LeagueUser.objects
                                     .select_related("league")
                                     .get(user_id=request.user.id))
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

            context = {'league_user': league_user,
                       'league': league,
                       'users': users}
        except (KeyError, LeagueUser.DoesNotExist):
            context = dict(must_have_league=True)

    return render(request, 'games/league.html', context)

@login_required
@transaction.atomic
def league_create(request):
    league_user = LeagueUser.objects.filter(user_id=request.user.id)
    if league_user.count() > 0:
        return HttpResponseForbidden("already_have_league")

    league_name = request.POST.get("league_name")
    league_check = League.objects.filter(name=league_name)
    if league_check.count() > 0:
        return HttpResponseForbidden("name_taken")

    league = League.create(name=league_name)
    LeagueUser.create(league_id=league.id, user_id=request.user.id,
                      admin=1, moderator=1)
    return HttpResponse("sucess")


@login_required
@transaction.atomic
def league_leave(request):
    if request.POST.get("data") != "pass":
        return HttpResponseForbidden("must_use_post")

    league_user = (LeagueUser.objects.get(user_id=request.user.id))

    if league_user.admin:
        league = league_user.league
        if league.leagueuser_set.count() > 1:
            return HttpResponseForbidden("must_empty_or_transfer_group")
        else:
            league_user.delete()
            league.delete()
    else:
        league_user.delete()

    return HttpResponse("sucess")

@login_required
@transaction.atomic
def league_remove_user(request):
    user_id = int(request.POST.get("data"))

    league_user = LeagueUser.objects.get(user_id=request.user.id)

    if not league_user.admin and not league_user.moderator:
        return HttpResponseForbidden("not_admin_nor_mod")

    if user_id == request.user.id:
        return HttpResponseForbidden("cannot_autoremove")

    league_user_to_delete = LeagueUser.objects.get(user_id=user_id)

    #Check if moderator is trying to remove another moderator or admin
    if (not league_user.admin and
        (league_user_to_delete.admin or
         league_user_to_delete.moderator)):
        return HttpResponseForbidden("cannot_remove_adm_nor_mod")

    league_user_to_delete.delete()
    return HttpResponse("sucess")

@login_required
@transaction.atomic
def league_add_or_remove_moderator(request, add):
    moderator_id = int(request.POST.get("data"))

    league_user = (LeagueUser.objects
                   .select_related("league")
                   .get(user_id=request.user.id))

    if not league_user.admin:
        if moderator_id != request.user.id or add: #allow auto-remove
             return HttpResponseForbidden("not_admin")

    mod = league_user.league.league_set.get(user_id=moderator_id)
    mod.moderator = add
    mod.save()
    return HttpResponse("sucess")

@login_required
@transaction.atomic
def league_add_moderator(request):
    return league_add_or_remove_moderator(request, 1)

@login_required
@transaction.atomic
def league_remove_moderator(request):
    return league_add_or_remove_moderator(request, 0)

@transaction.atomic
def league_add(request, user_id, league_id):
    LeagueUser.objects.create(user_id=user_id, league_id=league_id)

    (LeagueInvited.objects
                  .filter(user_id=user_id, league_id=league_id)
                  .delete())

    (LeagueAsked.objects
                .filter(user_id=user_id, league_id=league_id)
                .delete())

    return HttpResponse("sucess")

@transaction.atomic
def league_invite_join(request):
    invited_user_email = int(request.POST.get("data"))

    league_user = (LeagueUser.objects
                   .select_related("league")
                   .get(user_id=request.user.id))

    if not league_user.admin and not league_user.moderator:
        return HttpResponseForbidden("not_admin_nor_mod")



    return HttpResponse("sucess")

@transaction.atomic
def league_ask_join(request):
    league_id = int(request.POST.get("data"))

    league_user = (LeagueUser.objects
                   .select_related("league")
                   .get(user_id=request.user.id))

    if not league_user.admin and not league_user.moderator:
        return HttpResponseForbidden("not_admin_nor_mod")



    return HttpResponse("sucess")
