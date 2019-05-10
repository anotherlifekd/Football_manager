import requests
import random
import datetime
from celery import shared_task
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from time import sleep
from .models import Team, Match, Statistic


@shared_task
def team_score():
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


@shared_task
def score_update():
    useragent = UserAgent()
    headers = {
        'User-Agent': useragent.random,
    }

    COUNTRY = {'england': (2, 8), 'ukraine': (1, 7), 'germany': (3, 9), 'spain': (4, 10),
               'italy': (5, 11), 'netherlands': (6, 12), 'portugal': (7, 13), 'france': (8, 14)}

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
            Match.objects.filter(guest_team_id=guest.id, host_team_id=host.id).update(score_ended=score_ended)


@shared_task
def players_statistic():
    useragent = UserAgent()
    headers = {
        'User-Agent': useragent.random,
    }

    # 'italy': 5 DOESN'T WORK PAGE! PLEASE TRY LATER
    COUNTRY = {'england': 2, 'ukraine': 1, 'germany': 3, 'spain': 4, 'france': 8}

    for url in COUNTRY.keys():
        sleep(random.randint(3, 7))
        PAGE = 1
        while True:
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
                Statistic.objects.filter(name=name).update(team=team_id, games=int(games), goals=int(goals),
                                                           assists=int(assists), goal_plus_pass=int(goal_plus_pass),
                                                           yellow_cards=int(yellow_cards), red_cards=int(red_cards))


@shared_task
def team_info():
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