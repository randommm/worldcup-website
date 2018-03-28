from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import UserData
import requests

def index(request):
    return HttpResponseRedirect(reverse('accounts:login'))

def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('accounts:profile'))
    else:
        nextpage = request.GET.get('next')
        if not nextpage:
            nextpage = reverse('index')
        context = dict(nextpage = nextpage)
        return render(request, 'accounts/login.html', context)

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('accounts:login'))

@login_required
def rpass(request):
    try:
        user = User.objects.get(id=request.user.id)
        social = user.social_auth.filter(provider='google-oauth2')
        if len(social) > 0:
            response = requests.get(
                'https://www.googleapis.com/plus/v1/people/me',
                params={'access_token': social[0].extra_data['access_token']}
            )
        else:
            social = user.social_auth.filter(provider='facebook')
            response = requests.get(
                'https://graph.facebook.com/' + str(social[0].uid),
                params={'fields': 'id,name,locale,age_range,gender',
                'access_token': social[0].extra_data['access_token']}
            )

        extrainfo = response.json()

        user_data = UserData.objects.get_or_create(user=user)[0]
        user_data.data = extrainfo
        user_data.save()
    except Exception:
        pass

    return HttpResponseRedirect("/")

