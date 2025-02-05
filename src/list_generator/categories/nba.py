import requests


def fetch_data_nba(number_of_persons):
    url = "https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=PerGame&Scope=S&Season=2024-25&SeasonType=Regular%20Season&StatCategory=PTS"
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36"
    }

    response = requests.get(url)
    data = response.json()
    return data["resultSet"]["rowSet"][:number_of_persons]


def extract_full_names(person_list):
    return [person[2] for person in person_list]


def fetch_names_nba(number_of_persons):
    nba_list = fetch_data_nba(number_of_persons)
    full_names = extract_full_names(nba_list)
    return full_names
