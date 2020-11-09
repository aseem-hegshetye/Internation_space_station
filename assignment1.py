import json
import sys

import requests


class Iss:

    def __init__(self, func_type):
        self.func_type = func_type
        self.lat = None
        self.lon = None
        self.function_mapping = {
            'loc': self.loc,
            'pass': self.passing_detail,
            'people': self.people
        }

    def loc(self):
        url = 'http://api.open-notify.org/iss-now.json'
        response_json = self._get_json_response(url)
        timestamp = response_json["timestamp"]
        lat = response_json["iss_position"]["latitude"]
        lon = response_json["iss_position"]["longitude"]
        output = f'The ISS current location at {timestamp} ' \
                 f'is {lat, lon}'
        return output

    def passing_detail(self):
        url = 'http://api.open-notify.org/iss-pass.json'
        data = {
            'lat': self.lat,
            'lon': self.lon,
            'n': 1
        }
        response_json = self._get_json_response(url, data)

        if not response_json['response']:
            return 'No response for these lattitude and longitude'

        timestamp = response_json['response'][0]['risetime']
        duration = response_json['response'][0]['duration']
        output = f'The ISS will be overhead {self.lat, self.lon} at ' \
                 f'{timestamp} for {duration}'
        return output

    def people(self):
        url = 'http://api.open-notify.org/astros.json'
        response_json = self._get_json_response(url)
        no_of_people = response_json["number"]
        craft = response_json["people"][0]['craft']
        people_list = [p['name'] for p in response_json["people"]]
        output = f'There are {no_of_people} people aboard the {craft}. ' \
                 f'They are {people_list}'
        return output

    def execute(self):
        output = self.function_mapping[self.func_type]()
        print(output)

    def _get_json_response(self, url, data=None):
        response = requests.get(url, data)
        return json.loads(response.content)


if __name__ == '__main__':
    """
    Calling this python script:
    python assignment.py loc
    python assignment.py pass <lat> <lon>
    python assignment.py people
    """
    input_arg = sys.argv
    iss = Iss(input_arg[1])

    if input_arg[1] == 'pass':
        iss.lat = input_arg[2]
        iss.lon = input_arg[3]

    iss.execute()
