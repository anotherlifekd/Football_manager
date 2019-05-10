from rest_framework import serializers
from .models import Match, Team, Statistic, Country, Tournament


class MatchSerializer(serializers.ModelSerializer):

    country_name = serializers.CharField(source='country.name', read_only=True)
    host_team_name = serializers.CharField(source='host_team', read_only=True)
    guest_team_name = serializers.CharField(source='guest_team', read_only=True)
    tour_name = serializers.CharField(source='tour', read_only=True)

    class Meta:
        model = Match
        fields = ('id', 'country_name', 'tour_name', 'host_team_name', 'guest_team_name',
                  'date_and_time', 'score_ended', 'round')


class TeamSerializer(serializers.ModelSerializer):

    country_name = serializers.CharField(source='country.name', read_only=True)

    class Meta:
        model = Team
        fields = ('id', 'name', 'score', 'president', 'coach', 'stadium', 'foundation', 'site', 'country_name')


class StatisticSerializer(serializers.ModelSerializer):

    team_name = serializers.CharField(source='team.name', read_only=True)

    class Meta:
        model = Statistic
        fields = ('id', 'name', 'games', 'goals', 'assists', 'goal_plus_pass', 'yellow_cards', 'red_cards', 'team_name')


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ('id', 'name')


class TournamentSerializer(serializers.ModelSerializer):

    country_name = serializers.CharField(source='county.name', read_only=True)

    class Meta:
        model = Tournament
        fields = ('id', 'tournament', 'country_name')
