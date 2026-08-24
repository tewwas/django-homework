from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SportTournament(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name


class Match(models.Model):
    location = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    team1 = models.CharField(max_length=100)
    team2 = models.CharField(max_length=100)
    score_team1 = models.IntegerField(default=0)
    score_team2 = models.IntegerField(default=0)
    winner = models.CharField(max_length=100, blank=True, null=True)
    tournament = models.ForeignKey(
        SportTournament,
        on_delete=models.CASCADE,
        related_name="matches",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.team1} - {self.team2}"