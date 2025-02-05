import requests


def fetch_data_billionaires(number_of_persons):
    url = "https://www.forbes.com/forbesapi/person/billionaires/2024/position/true.json?fields=uri,finalWorth,age,country,source,rank,category,personName,industries,organization,gender,firstName,lastName,squareImage,bios,status,countryOfCitizenship"
    response = requests.get(url)
    data = response.json()
    return data["personList"]["personsLists"][:number_of_persons]


def extract_full_names(person_list):
    return [
        f"{person['firstName']} {person['lastName']}".replace(" & family", "")
        for person in person_list
    ]


def fetch_names_billionaires(number_of_persons):
    billionaire_list = fetch_data_billionaires(number_of_persons)
    full_names = extract_full_names(billionaire_list)
    return full_names
