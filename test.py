import requests
from pprint import pprint
from typing import List, AnyStr


class StarWarsHandler:
    def __init__(self):
        self.results: list = []
        self.list_start_wars_basic()

    def list_start_wars_basic(self):
        address = "https://swapi.dev/api/people/?page={}"

        counter = 1
        timeout = 30

        while counter <= timeout:
            response = requests.get(address.format(counter)).json()

            if response == {'detail': 'Not found'}:
                pprint('end of list')
                break

            for item in response["results"]:
                # print(item)
                self.results.append(item)
            counter += 1

    def list_star_wars_height(self, by_height=100):
        for item in self.results:
            try:
                if int(item.get("height", 0)) > by_height:
                    pprint(item.get('height', 0))
            except ValueError as err:
                pass

    def get_by_name(self, name: str):
        for item in self.results:
            try:
                if item.get('name', None) == name:
                    print(item)
            except ValueError:
                pass

    def get_list_of_names(self, names: List[AnyStr]):

        for character in self.results:
            if character['name'] in names:
                print('we got it')


if __name__ == '__main__':
    sw_handler = StarWarsHandler()
    print(sw_handler.get_by_name(name='R2-D2'))

    sw_handler.get_list_of_names(names=[
        'R2-D2',
        'Luke Skywalker',
        "Darth Vader"
    ])
