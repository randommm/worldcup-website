from django.db import models
from django.contrib.auth.models import User

#User._meta.get_field('email')._unique = True

class Team(models.Model):
    name = models.CharField(max_length=200, unique=True)
    flag = models.CharField(max_length=200, default="xx")

    def __str__(self):
        return self.name

class Game(models.Model):
    team0 = models.ForeignKey(Team, related_name="team0", on_delete=models.CASCADE)
    team1 = models.ForeignKey(Team, related_name="team1", on_delete=models.CASCADE)
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return str(self.user)

class Result(models.Model):
    game = models.OneToOneField(Game, on_delete=models.CASCADE)
    result = models.PositiveSmallIntegerField()
    committed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.game)
