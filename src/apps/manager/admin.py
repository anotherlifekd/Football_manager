from django.contrib import admin
from .models import Country, Tournament, Team, Statistic, Match


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    readonly_fields = ('name', )


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    readonly_fields = ('tournament', 'county')
    list_display = ['tournament', 'county']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    readonly_fields = ('name', 'score', 'country', 'stadium', 'foundation', 'team_url')
    list_display = ['name', 'score', 'country', 'site']
    list_filter = ['country']
    list_per_page = 15
    search_fields = ['name', 'stadium', 'country__name', 'president', 'coach']


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    readonly_fields = ('name', 'team', 'games', 'goals', 'assists', 'goal_plus_pass', 'yellow_cards', 'red_cards')
    list_display = ['name', 'team', 'games', 'goals', 'assists', 'goal_plus_pass', 'yellow_cards', 'red_cards']
    list_filter = ['team__country', 'team']
    search_fields = ['name', 'team__name', 'team__country__name']


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    readonly_fields = ('country', 'tour', 'host_team', 'guest_team', 'score_ended', 'round')
    list_display = ['host_team', 'score_ended', 'guest_team', 'round', 'tour', 'country']
    list_filter = ['tour', 'country']
    list_per_page = 20
    search_fields = ['country__name', 'host_team__name', 'guest_team__name']
    list_display_links = ('score_ended', )
