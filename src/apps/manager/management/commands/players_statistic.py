import requests
from bs4 import BeautifulSoup
from time import sleep
import random
from django.core.management.base import BaseCommand
from apps.manager.models import Statistic, Team
from fake_useragent import UserAgent


class Command(BaseCommand):

    def handle(self, *args, **options):
        useragent = UserAgent()
        headers = {
            'User-Agent': useragent.random,
        }

        # 'italy': 5 DOESN'T WORK PAGE! PLEASE TRY LATER
        COUNTRY = {'england': 2, 'ukraine': 1, 'germany': 3, 'spain': 4, 'france': 8}

        result = []

        for url in COUNTRY.keys():
            sleep(random.randint(3, 7))
            PAGE = 1
            while True:
                print(f'======================={PAGE} ----------- {url}=======================')
                sleep(random.randint(3, 7))
                COUNTRY_URL_PAGE = f'https://football.ua/{url}/statistics/p{PAGE}.html'

                response = requests.get(COUNTRY_URL_PAGE, headers=headers)
                try:
                    assert response.status_code == 200
                except AssertionError:
                    COUNTRY_URL_PAGE = f'https://football.ua/{url}/statistics/{PAGE}.html'

                PAGE += 1
                response = requests.get(COUNTRY_URL_PAGE, headers=headers)
                assert response.status_code == 200
                html_doc = response.text
                soup = BeautifulSoup(html_doc, 'html.parser')

                statistic_table = soup.find('table', {'class': 'statistic-table'})
                if statistic_table is None:
                    break
                statistic_table_items = statistic_table.find_all('tr')
                for item in statistic_table_items[1:]:
                    team = item.find('td', {'class': 'flag'}).find('a', href=True)['title']
                    name = item.find('td', {'class': 'name'}).find('a').text
                    games = item.find('td', {'class': 'games'}).text
                    goals = item.find('td', {'class': 'goals'}).text
                    if '(' in goals:
                        goals = goals[:goals.index('(')]
                    assists = item.find('td', {'class': 'passes'}).text
                    goal_plus_pass = item.find('td', {'class': 'goal-pass'}).text
                    yellow_cards = item.find('td', {'class': 'yellow-card'}).text
                    red_cards = item.find('td', {'class': 'red-card'}).text
                    if team is None:
                        continue

                    team_id = Team.objects.get(name=team)
                    Statistic.objects.create(team=team_id, name=name, games=int(games), goals=int(goals), assists=int(assists),
                                             goal_plus_pass=int(goal_plus_pass), yellow_cards=int(yellow_cards),
                                             red_cards=int(red_cards))
        #             statistic = Statistic(team=team_id, name=name, games=int(games), goals=int(goals),
        #                                   assists=int(assists), goal_plus_pass=int(goal_plus_pass),
        #                                   yellow_cards=int(yellow_cards), red_cards=int(red_cards))
        #             result.append(statistic)
        # Team.objects.bulk_create(result)
