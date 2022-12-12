import requests
import datetime

def get_people(people):

    return requests.get(f'https://swapi.dev/api/{people}/').json()

def main():
    print(get_people(people='people'))

start = datetime.datetime.now()

main()

print(datetime.datetime.now() - start)