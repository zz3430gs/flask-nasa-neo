import os
import requests

API_KEY = os.getenv('NEO_API_KEY', 'DEMO_KEY')
BASE_URL = 'https://api.nasa.gov/neo/rest/v1/'


class NearEarthObject:
    def __init__(self, neo_id, name, url, diameter_min, diameter_max, hazardous,
                 approaches):
        self.id = neo_id
        self.name = name
        self.url = url
        self.diameter_min = '{:.2f}'.format(float(diameter_min))
        self.diameter_max = '{:.2f}'.format(float(diameter_max))
        self.hazardous = hazardous
        self.approaches = approaches

    @classmethod
    def from_json(cls, data):
        neo_id = data['neo_reference_id']
        name = data['name']
        url = data['nasa_jpl_url']
        diameter_min = (data['estimated_diameter']
                        ['feet']['estimated_diameter_min'])
        diameter_max = (data['estimated_diameter']
                        ['feet']['estimated_diameter_max'])
        hazardous = data['is_potentially_hazardous_asteroid']
        approaches = [Approach.from_json(approach)
                      for approach in data['close_approach_data']]

        return cls(neo_id, name, url, diameter_min, diameter_max, hazardous,
                   approaches)


class Approach:
    def __init__(self, date, velocity, distance, orbiting_body):
        self.date = date
        self.velocity = '{:.2f}'.format(float(velocity))
        self.distance = '{:.2f}'.format(float(distance))
        self.orbiting_body = orbiting_body

    @classmethod
    def from_json(cls, data):
        date = data['close_approach_date']
        velocity = data['relative_velocity']['miles_per_hour']
        distance = data['miss_distance']['miles']
        orbiting_body = data['orbiting_body']
        return cls(date, velocity, distance, orbiting_body)


def today(detailed=False):
    url = '{base}/feed/today?detailed={detailed}&api_key={key}'.format(
        base=BASE_URL,
        detailed=str(detailed).lower(),
        key=API_KEY,
    )

    res = requests.get(url)
    data = res.json()

    return [NearEarthObject.from_json(neo)
            for date in data['near_earth_objects']
            for neo in data['near_earth_objects'][date]]


def details(neo_id):
    url = '{base}/neo/{neo_id}?api_key={key}'.format(
        base=BASE_URL,
        neo_id=neo_id,
        key=API_KEY,
    )

    res = requests.get(url)
    if res.status_code != 200:
        return

    data = res.json()

    return NearEarthObject.from_json(data)
