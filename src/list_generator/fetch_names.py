from src.list_generator.categories.billionaires import fetch_names_billionaires
from src.list_generator.categories.kpop import fetch_names_kpop
from src.list_generator.categories.nba import fetch_names_nba
from src.list_generator.categories.us_artists import fetch_names_us_artists
from src.list_generator.categories.us_politicians import fetch_names_us_politicians


def fetch_names(category, number_of_persons):
    if category == "billionaires":
        return fetch_names_billionaires(number_of_persons)
    if category == "kpop":
        return fetch_names_kpop(number_of_persons)
    if category == "nba":
        return fetch_names_nba(number_of_persons)
    if category == "us_artists":
        return fetch_names_us_artists(number_of_persons)
    if category == "us_politicians":
        return fetch_names_us_politicians(number_of_persons)
