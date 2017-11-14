from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import logout

def index(request):
    return HttpResponseRedirect(reverse('accounts:login'))

def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('accounts:profile'))
    else:
        return render(request, 'accounts/login.html')

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('accounts:login'))
