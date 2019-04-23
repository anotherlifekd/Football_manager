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
        # Team.objects.all().delete()
        COUNTRY = {'england': 2, 'ukraine': 1, 'germany': 3, 'spain': 4,
                   'italy': 5, 'netherlands': 6, 'portugal': 7, 'france': 8}
        result = []
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
                a = name.find('a', href=True)
                url_team = a['href']
                team_url = url_team[url_team.rindex('/')+1:-5]
                new_team = Team(name=team.text.strip(), score=score.text,
                                country_id=COUNTRY.get(url), team_url=team_url)
                result.append(new_team)
        Team.objects.bulk_create(result)

