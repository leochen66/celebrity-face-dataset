import re
import json
import requests
from bs4 import BeautifulSoup


def fetch_data_us_politicians(number_of_persons):
    try:
        offset = 0
        limit = 20
        person_names = []
        base_url = "https://today.yougov.com/_pubapis/v5/us/search/entity/?group=07df945a-adf0-11e9-9161-317b338eee4b&sort_by=popularity&"
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36"
        }

        while len(person_names) < number_of_persons:
            remaining = number_of_persons - len(person_names)
            current_limit = min(limit, remaining)

            url = f"{base_url}limit={current_limit}&offset={offset}"
            # print(f"Fetching: {url}")

            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                data_names = [person["name"] for person in data["data"]]
                person_names.extend(data_names)
            else:
                print(f"Failed to fetch data: {response.status_code}")
                break

            offset += current_limit

        return person_names

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error fetching data from the URL: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding JSON data: {e}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {e}")


def fetch_names_us_politicians(number_of_persons):
    full_names = fetch_data_us_politicians(number_of_persons)
    return full_names
