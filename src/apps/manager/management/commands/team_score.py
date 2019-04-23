import requests
from bs4 import BeautifulSoup
from time import sleep
import random
from django.core.management.base import BaseCommand
from apps.manager.models import Team
from fake_useragent import UserAgent


class Command(BaseCommand):
    help = 'Create test data'

    def handle(self, *args, **options):
        useragent = UserAgent()
        headers = {
            'User-Agent': useragent.random,
        }
        COUNTRY = {'england': 2, 'ukraine': 1, 'germany': 3, 'spain': 4,
                   'italy': 5, 'netherlands': 6, 'portugal': 7, 'france': 8}
        for url in COUNTRY.keys():
            sleep(random.randint(3, 7))
            URL_COUNTRY = f'https://football.ua/{url}/table.html'

            response = requests.get(URL_COUNTRY, headers=headers)
            assert response.status_code == 200
            html_doc = response.text
            soup = BeautifulSoup(html_doc, 'html.parser')
            table = soup.find('table', {'class': 'main-tournament-table'})
            test_team = table.find_all('tr')
            for name in test_team[1:]:
                team = name.find('td', {'class': 'team'})
                score = name.find('td', {'class': 'score'})
                if team is None or score is None:
                    continue
                Team.objects.filter(name=team.text.strip()).update(score=score.text)
