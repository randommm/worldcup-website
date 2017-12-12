from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth.models import User
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
    user = User.objects.get(id=request.user.id)
    social = user.social_auth.get(provider='google-oauth2')
    response = requests.get(
        'https://www.googleapis.com/plus/v1/people/me',
        params={'access_token': social.extra_data['access_token']}
    )
    extrainfo = response.json()
    context = dict(extrainfo = extrainfo)
    return render(request, 'accounts/profile.html', context)

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('accounts:login'))
