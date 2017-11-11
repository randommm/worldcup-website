from django.contrib import admin

# Register your models here.
from .models import User, Team, Game, Bet, Predict, Result

admin.site.register([User, Team, Game, Bet, Predict, Result])
