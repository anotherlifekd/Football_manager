from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=11, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Countries"


class Tournament(models.Model):
    tournament = models.CharField(max_length=20, unique=True)
    county = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='tournament')

    def __str__(self):
        return self.tournament

    class Meta:
        verbose_name_plural = "Tournaments"


class Team(models.Model):
    name = models.CharField(max_length=32, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='team')
    score = models.SmallIntegerField()

    # info
    president = models.CharField(max_length=32, blank=True, null=True)
    coach = models.CharField(max_length=32, blank=True, null=True)
    stadium = models.CharField(max_length=64, blank=True, null=True)
    foundation = models.SmallIntegerField(blank=True, null=True)
    site = models.URLField(max_length=128, unique=True, blank=True, null=True)
    team_url = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Teams"


class Statistic(models.Model):
    name = models.CharField(max_length=64)
    games = models.SmallIntegerField(blank=True, null=True)
    goals = models.SmallIntegerField(blank=True, null=True)
    assists = models.SmallIntegerField(blank=True, null=True)
    goal_plus_pass = models.SmallIntegerField(blank=True, null=True)
    yellow_cards = models.SmallIntegerField(blank=True, null=True)
    red_cards = models.SmallIntegerField(blank=True, null=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='statistic')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Statistic"


class Match(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='country')
    tour = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='tour')
    host_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='host_team')
    guest_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='guest_team')
    date_and_time = models.DateTimeField(blank=True, null=True)
    score_ended = models.CharField(max_length=5, blank=True, null=True)
    round = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.host_team} - {self.guest_team}'

    class Meta:
        verbose_name_plural = "Matches"
