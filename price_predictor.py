import re
import statistics
import pandas as pd

import matplotlib.pyplot as plt

#from cheap_flights_crawler import fill_data
from cheap_flights_crawler import fill_data
from flight_search import Flights
from kiwi_researcher import kiwi_create_dataset

flight = Flights('WAW', 'YTO', '2021-02-28', '2021-03-10')

try:
    # fly_from = flight.get_fly_from()
    ch_fl_df = fill_data(flight)
    print('Set created')
except:
    pass
    print("Set has not been created, let's try again")
    ch_fl_df = fill_data(flight)
# data storage
cheap_flights_prices = ch_fl_df['price'].to_list()
cheap_flights_airlines = ch_fl_df['airline'].to_list()
converted_price_list = [re.sub(r'[^0-9]', '', price) for price in cheap_flights_prices]
print(converted_price_list)
price_list = [int(i) for i in converted_price_list]


kiwi_df = kiwi_create_dataset(flight)
kiwi_prices = kiwi_df['price'].to_list()
kiwi_airlines = kiwi_df['airlines'].to_list()
kiwi_airlines = [re.sub(r'[^a-zA-Z]*', '',str(value)) for value in kiwi_airlines]
#kiwi_airlines = [str(airline).strip('[]') for airline in kiwi_airlines]
#print(kiwi_prices)

# matplotlib generating plots

def predict(prices_list, airlines_list):
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, facecolor='#FFFFCC')
    plt.xlabel('Airlines')
    plt.ylabel('Prices in £')
    plt.title('Price per airline reported by kiwi')
    # counting specific valuees

    average = statistics.mean(prices_list)
    minimum = min(prices_list)

    ax.plot(airlines_list, prices_list, 'o')

    # printing values in plot
    # plt.text(average, average, 'average equals to : {}'.format(average))

    # average y line
    ax.axhline(average, color='k', linestyle='dashed', linewidth=2.0)
    ax.axhline(minimum, color='r', linestyle=':', linewidth=2.0)

    plt.text(0.25, minimum, 'minimum equals to :  {}'.format(minimum))
    plt.text(0.25, average, 'average equals to : {}'.format(average))
    plt.show()
    list1 = list(zip(airlines_list,prices_list))
    df = pd.DataFrame(list1,columns=['airlines','prices'])
    average = df.groupby('airlines').mean()
    print(average.head(9))

    def make_autopct(values):
        def my_autopct(pct):
            total = sum(values)
            val = int(round(pct * total / 100.0))
            return '{v:d}'.format(v=val)

        return my_autopct

    plot = average.plot.pie(y='prices', autopct=make_autopct(average['prices']))
    plt.show()




prices_list = price_list + kiwi_prices
airlines_list = cheap_flights_airlines + kiwi_airlines
predict(prices_list, airlines_list)
