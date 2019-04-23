import requests
from bs4 import BeautifulSoup
from time import sleep
import random
from fake_useragent import UserAgent
from django.core.management.base import BaseCommand
from apps.manager.models import Team


class Command(BaseCommand):
    def handle(self, *args, **options):
        result = []
        useragent = UserAgent()
        headers = {
            'User-Agent': useragent.random,
        }
        for url in Team.objects.all().values_list('team_url', flat=True):
            sleep(random.randint(3, 7))
            print(url)
            MAIN_URL = f'https://football.ua/club/{url}.html'
            response = requests.get(MAIN_URL, headers=headers)
            assert response.status_code == 200
            html_doc = response.text
            soup = BeautifulSoup(html_doc, 'html.parser')
            table = soup.find('table', {'class': 'info-page-table'})
            info_detail = table.findAll('td')
            full_info = {'Президент:': None, 'Главный тренер:': None, 'Стадион:': None, 'Год основания:': None,
                         'Сайт клуба:': None}
            for item in range(len(info_detail)):
                clear_item = info_detail[item].text.strip()
                if clear_item in full_info.keys():
                    full_info[clear_item] = info_detail[item + 1].text.strip()
            Team.objects.filter(team_url=url).update(president=full_info['Президент:'], coach=full_info['Главный тренер:'],
                                stadium=full_info['Стадион:'], foundation=full_info['Год основания:'],
                                site=full_info['Сайт клуба:'])






