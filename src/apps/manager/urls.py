from django.urls import path
from .views import *

from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='API')
app_name = "manager"

urlpatterns = [
    path('matches/', MatchView.as_view()),
    path('teams/', TeamsView.as_view()),
    path('statistic/', StatisticView.as_view()),
    path('country/', CountryView.as_view()),
    path('tournaments/', TournamentView.as_view()),
    #path('docs/', schema_view),
]