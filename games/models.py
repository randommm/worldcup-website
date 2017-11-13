from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

class Game(models.Model):
    team1 = models.ForeignKey(Team, related_name="team1", on_delete=models.CASCADE)
    team2 = models.ForeignKey(Team, related_name="team2", on_delete=models.CASCADE)
    date = models.DateTimeField('Game date')

    class Meta:
        unique_together = ("team1", "team2", "date")

    def __str__(self):
        return self.team1.name + " vs " + self.team2.name

class Bet(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prob1 = models.PositiveSmallIntegerField()
    prob2 = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ("game", "user")

    def __str__(self):
        return str(self.game) + " by user " + self.user.name

class Forecast(models.Model):
    game = models.OneToOneField(Game, on_delete=models.CASCADE)
    prob1 = models.PositiveSmallIntegerField()
    prob2 = models.PositiveSmallIntegerField()

    def __str__(self):
        return str(self.game)

class Result(models.Model):
    game = models.OneToOneField(Game, on_delete=models.CASCADE)
    result = models.PositiveSmallIntegerField()

    def __str__(self):
        return str(self.game)
