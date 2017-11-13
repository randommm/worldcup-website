from django.contrib import admin

# Register your models here.
from .models import User2, Team, Game, Bet, Forecast, Result

admin.site.register([User, Team, Game, Bet, Forecast, Result])
