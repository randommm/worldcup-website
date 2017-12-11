from django.db import models
from django.contrib.auth.models import User

#User._meta.get_field('email')._unique = True

class Team(models.Model):
    name = models.CharField(max_length=200, unique=True)
    flag = models.CharField(max_length=200, default="xx")

    def __str__(self):
        return self.name

class Game(models.Model):
    team0 = models.ForeignKey(Team, related_name="game_team0_set", on_delete=models.CASCADE)
    team1 = models.ForeignKey(Team, related_name="game_team1_set", on_delete=models.CASCADE)
    date = models.DateTimeField('Game date')

    class Meta:
        unique_together = ("team0", "team1", "date")

    def __str__(self):
        return self.team0.name + " vs " + self.team1.name

class Bet(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prob0 = models.PositiveSmallIntegerField()
    prob1 = models.PositiveSmallIntegerField()
    points = models.IntegerField(default=-1)

    class Meta:
        unique_together = ("game", "user")

    def __str__(self):
        return str(self.game) + " by " + self.user.email

class Point(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True)
    points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.user)

class Result(models.Model):
    game = models.OneToOneField(Game, on_delete=models.CASCADE,
                                primary_key=True)
    result = models.PositiveSmallIntegerField()
    committed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.game)

class League(models.Model):
    name = models.CharField(max_length=100, default="xx", unique=True)
    kind = models.PositiveSmallIntegerField(default=0)
    points = models.PositiveIntegerField(default=0)
    user_count = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return str(self.name)

class LeagueUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    admin = models.BooleanField(default=False)
    moderator = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "league")

    def __str__(self):
        return str(self.user)

class LeagueAsked(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    rejected = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user) + str(self.league)
