import re
import json
import requests
from bs4 import BeautifulSoup


def fetch_data_us_artists(number_of_persons):
    url = "https://www.billboard.com/charts/artist-100"
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, "lxml")

        person_sections = soup.select(".o-chart-results-list-row-container")[
            :number_of_persons
        ]
        person_names = [
            person_section.select("#title-of-a-story")[0]
            .text.lstrip()
            .replace("\n", "")
            .replace("\t", "")
            for person_section in person_sections
        ]

        return person_names

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error fetching data from the URL: {e}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {e}")


def fetch_names_us_artists(number_of_persons):
    full_names = fetch_data_us_artists(number_of_persons)
    return full_names
