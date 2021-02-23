import urllib.request
import json
import pandas as pd
from flight_search import Flights
from datetime import datetime


def convert_date(date):
    converted_date = date[8:] + "/" + date[5:7] + "/" + date[:4]
    return converted_date


def kiwi_create_dataset(flight):
    date_from = flight.get_date_from()
    date_to = flight.get_date_to()
    kiwi_date_from = convert_date(date_from)
    kiwi_date_to = convert_date(date_to)

    url = 'https://api.skypicker.com/flights?fly_from={0}&fly_to={1}&locale=pl-PL&partner=picky&date_from={2}&' \
          'date_to={3}&curr=GBP'.format(flight.get_fly_from(), flight.get_fly_to(), kiwi_date_from, kiwi_date_to)
    json_obj = urllib.request.urlopen(url)
    kiwi_data = json.load(json_obj)
    with open('airlines.json') as json_file:
        airline_list = json.load(json_file)
    airline_dict = {}

    for item in airline_list:
        code = item.pop('code')
        airline_dict[code] = item

    travel_list = []
    for item in kiwi_data['data']:
        dDate = datetime.fromtimestamp(item['dTimeUTC'])
        aDate = datetime.fromtimestamp(item['aTimeUTC'])
        airlines = []

        for key, values in airline_dict.items():
            if key in item['airlines']:
                airlines.append(values)
                if len(airlines) == 1:
                    airlines = [d['name'] for d in airlines]


                else:
                    airlines = ["Multiple Airlines"]
                # print(len(airlines))

        travel_list.append([dDate, aDate, item['flyFrom'], item['flyTo'], airlines,
                            item['price'], item['deep_link']])

    dataset = pd.DataFrame(travel_list)
    dataset.columns = ['dTime', 'aTime', 'flyFrom', 'flyTo', 'airlines', 'price', 'deep_link']
    return dataset


