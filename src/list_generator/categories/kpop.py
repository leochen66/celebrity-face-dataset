import re
import json
import requests
from bs4 import BeautifulSoup


def fetch_data_kpop(number_of_persons):
    url = "https://www.billboard.com/lists/k-pop-artist-100-list-2024-ranked"
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, "lxml")

        script_tag = soup.select_one("#pmc-lists-front-js-extra")
        if not script_tag:
            raise ValueError("Script tag with required data not found.")

        script_content = script_tag.text
        match = re.search(r"var pmcGalleryExports = (.*?)};", script_content, re.DOTALL)
        if not match:
            raise ValueError(
                "Required data (pmcGalleryExports) not found in the script tag."
            )

        person_data = match.group(1) + "}"  # Add the missing closing brace
        person_json = json.loads(person_data)
        person_json = person_json.get("gallery", [])

        return person_json[:number_of_persons]

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error fetching data from the URL: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding JSON data: {e}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {e}")


def extract_full_names(person_list):
    return [person.get("title") for person in person_list]


def fetch_names_kpop(number_of_persons):
    kpop_list = fetch_data_kpop(number_of_persons)
    full_names = extract_full_names(kpop_list)
    return full_names
