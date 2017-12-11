from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.urls import reverse
from .models import User, Team, Game, Bet, Result, Point, League
from .models import LeagueUser, LeagueInvited, LeagueAsked
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
        return HttpResponseForbidden("user_have_league")

    league_name = request.POST.get("league_name")
    league_check = League.objects.filter(name=league_name)
    if league_check.count() > 0:
        return HttpResponseForbidden("name_taken")

    league = League.objects.create(name=league_name)
    LeagueUser.objects.create(league_id=league.id,
                              user_id=request.user.id,
                              admin=1, moderator=1)
    return HttpResponse("success")


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
    return HttpResponse("success")



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




@login_required
@transaction.atomic
def league_add(request, user_id, league_id):
    (LeagueInvited.objects
                  .filter(user_id=user_id, league_id=league_id)
                  .delete())

    (LeagueAsked.objects
                .filter(user_id=user_id, league_id=league_id)
                .delete())

    LeagueUser.objects.create(user_id=user_id, league_id=league_id)

    return HttpResponse("success")

@login_required
@transaction.atomic
def league_ask_join(request):
    league_id = int(request.POST.get("data"))
    user_id=request.user.id

    check_member = LeagueUser.objects.filter(user_id=user_id)
    if check_member.count() > 0:
        return HttpResponseForbidden("user_already_has_league")

    check_league = League.objects.filter(league_id=league_id)
    if check_league.count() > 11:
        return HttpResponseForbidden("league_full")


    LeagueAsked.objects.create(user_id=p_user_id, league_id=league_id)

    if LeagueInvited.objects.filter(user_id=p_user_id,
                                    league_id=league_id).count():
        return league_add(user_id, league_id)

    return HttpResponse("success")










@login_required
@transaction.atomic
def league_invite_join(request):
    p_user_email = request.POST.get("data")

    a_league_user = (LeagueUser.objects
                   .select_related("league")
                   .get(user_id=request.user.id))

    league_id = a_league_user.league.id

    if not a_league_user.admin and not a_league_user.moderator:
        return HttpResponseForbidden("not_admin_nor_mod")

    p_user_id_all = User.objects.filter(email=p_user_email)
    if p_user_id_all.count() == 0:
        return HttpResponseForbidden("invalid_email")
    elif p_user_id_all.count() > 1:
        return HttpResponseForbidden("multiple_users_with_same_email")
    p_user_id = p_user_id_all[0].id

    check_member = LeagueUser.objects.filter(user_id=p_user_id)
    if check_member.count() > 0:
        return HttpResponseForbidden("user_already_has_league")

    check_league = League.objects.filter(league_id=league_id)
    if check_league.count() > 11:
        return HttpResponseForbidden("league_full")

    LeagueInvited.objects.create(user_id=p_user_id, league_id=league_id)

    if LeagueAsked.objects.filter(user_id=p_user_id,
                                  league_id=league_id).count():
        return league_add(user_id, league_id)

    return HttpResponse("success")
