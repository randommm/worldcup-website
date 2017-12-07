from django.contrib import admin

# Register your models here.
from .models import Team, Game, Bet, Result

admin.site.register([Team, Game, Bet, Result])
