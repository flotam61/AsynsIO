import requests
import datetime



def get_list_in_url(id_data):
    films_list = []
    for i in id_data['films']:
        films_data = requests.get(f'{i}').json()
        films_list.append(films_data['title'])
    id_data.update({'films': films_list})
    speciec_list = []
    for i in id_data['species']:
        speciec_data = requests.get(f'{i}').json()
        speciec_list.append(speciec_data['name'])
    id_data.update({'species': speciec_list})
    starships_list = []
    for i in id_data['starships']:
        starships_data = requests.get(f'{i}').json()
        starships_list.append(starships_data['name'])
    id_data.update({'starships': starships_list})
    vehicles_list = []
    for i in id_data['vehicles']:
        vehicles_data = requests.get(f'{i}').json()
        vehicles_list.append(vehicles_data['name'])
    id_data.update({'vehicles': vehicles_list})

    return id_data

def get_people(people_id):


    data = requests.get(f'https://swapi.dev/api/people/{people_id}').json()
    print(data)
    if 'detail' not in data:
        print('net')
    else:
        print('da')
    # data_new = get_list_in_url(data)
    # print(data_new)
    return data


def main():
    for i in range(17, 19):
        get_people(i)

start = datetime.datetime.now()

main()

print(datetime.datetime.now() - start)