from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Match, Team, Statistic, Country, Tournament
from .serializers import MatchSerializer, TeamSerializer, StatisticSerializer, CountrySerializer, TournamentSerializer

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter


# class MatchApi(APIView):
#     permission_classes = [AllowAny]
#     def get(self, request):
#         matches = Match.objects.all()
#         filter_fields = ('country', 'tour')
#         serializer = MatchSerializer(matches, many=True)
#         return Response({'data': serializer.data})


# class TeamApi(APIView):
#
#     # permission_classes = [permissions.AllowAny, ]
#
#     def get(self, request):
#         teams = Team.objects.all()
#         serializer = TeamSerializer(teams, many=True)
#         return Response({'data': serializer.data})

class CountryView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CountrySerializer
    queryset = Country.objects.all()


class TournamentView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = TournamentSerializer
    queryset = Tournament.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('county__name',)


class MatchView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = MatchSerializer
    queryset = Match.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ('id', 'country__name', 'tour', 'host_team', 'guest_team', 'date_and_time', 'score_ended', 'round')
    ordering_fields = ('country__name', 'tour', 'host_team', 'guest_team', 'date_and_time', 'round')
    search_fields = ('country__name', 'host_team__name', 'guest_team__name')


class TeamsView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = TeamSerializer
    queryset = Team.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ('name', 'score', 'foundation', 'country')
    ordering_fields = ('name', 'score', 'foundation', 'country')
    search_fields = ('name', 'country__name')


class StatisticView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = StatisticSerializer
    queryset = Statistic.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ('games', 'goals', 'team')
    ordering_fields = ('games', 'goals')
    search_fields = ('name', 'team__name')


def index(request):
    return render(request, 'index.html')
