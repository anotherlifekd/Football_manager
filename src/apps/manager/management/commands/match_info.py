import requests
from bs4 import BeautifulSoup
from time import sleep
import random
import datetime
from fake_useragent import UserAgent
from django.core.management.base import BaseCommand
from apps.manager.models import Match, Team


class Command(BaseCommand):

    def handle(self, *args, **options):
        Match.objects.all().delete()
        useragent = UserAgent()
        headers = {
            'User-Agent': useragent.random,
        }

        COUNTRY = {'england': (2, 8), 'ukraine': (1, 7), 'germany': (3, 9), 'spain': (4, 10),
                   'italy': (5, 11), 'netherlands': (6, 12), 'portugal': (7, 13), 'france': (8, 14)}

        result = []

        for url in COUNTRY.keys():
            sleep(random.randint(3, 7))
            COUNTRY_URL = f'https://football.ua/{url}/results/'

            response = requests.get(COUNTRY_URL, headers=headers)
            assert response.status_code == 200
            html_doc = response.text
            soup = BeautifulSoup(html_doc, 'html.parser')

            table = soup.find('div', {'class': 'table-block'})
            match_list = table.find_all('div', {'class': 'match'})

            list_url = []
            for match in match_list:
                match_url = match.find('td', {'class': 'score'})
                link = match_url.find('a', href=True)
                get_link = link['href']
                short_link = get_link[get_link.rindex('/') + 1:-5]
                list_url.append(short_link)

            for match in list_url:
                sleep(random.randint(3, 7))
                MATCH_URL = f'https://football.ua/england/game/{match}.html'

                response = requests.get(MATCH_URL, headers=headers)
                assert response.status_code == 200
                html_doc = response.text
                soup = BeautifulSoup(html_doc, 'html.parser')

                match_full_info = soup.find('div', {'class': 'col-top'})
                match_details = match_full_info.find('article', {'class': 'match-details'})

                # TOUR
                tour = ''.join(filter(lambda x: x.isdigit(), match_details.h3.text))

                # SCORE AND TEAMS_ID
                match_details_teams = match_details.find('div', {'class': 'match-details-teams'})

                left_team = match_details_teams.find('div', {'class': 'left-team'})
                host_team = left_team.text.strip()

                right_team = match_details_teams.find('div', {'class': 'right-team'})
                guest_team = right_team.text.strip()

                score = match_details_teams.find('div', {'class': 'score'})
                match_score = score.find_all('span')
                score_ended = f'{match_score[0].text}:{match_score[1].text}'

                # DATE AND TIME
                match_info = match_full_info.find('article', {'class': 'match-info'})
                match_info_table = match_info.find_all('tr')
                full_date_info = match_info_table[-1].text.replace(',', '').split()
                if full_date_info[3] == '--:--':
                    full_date_info[3] = '00:00'
                date_and_time = ' '.join(full_date_info[2:4]).replace('.', '-')

                datetime_str = date_and_time
                old_format = '%d-%m-%Y %H:%M'
                new_format = '%Y-%m-%d %H:%M'
                new_datetime_str = datetime.datetime.strptime(datetime_str, old_format).strftime(new_format)

                # ADD TO BASE
                host = Team.objects.get(name=host_team)
                guest = Team.objects.get(name=guest_team)
                print(MATCH_URL, host, guest, score_ended)
                # Match.objects.create(date_and_time=new_datetime_str, score_ended=score_ended, round=tour,
                #                      country_id=COUNTRY[url][0], guest_team_id=guest.id, host_team_id=host.id,
                #                      tour_id=COUNTRY[url][1])
        #         new_match = Match(date_and_time=date_and_time, score_ended=score_ended, round=tour,
        #                           country_id=COUNTRY[url][0], guest_team_id=guest.id, host_team_id=host.id,
        #                           tour_id=COUNTRY[url][1])
        #         result.append(new_match)
        #
        # Match.objects.bulk_create(result)
                # print(f'tour: {tour}, host_team: {host_team}, guest_team: {guest_team}, score_ended: {score_ended},'
                #       f'date: {date_and_time}, country: {COUNTRY[url][0]}, tournament: {COUNTRY[url][1]}')