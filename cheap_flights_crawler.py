from selenium import webdriver
from selenium.webdriver import TouchActions, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
import re
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

from flight_search import Flights

value_privacy_accept = '//*[@title="Accept"]'



# initialize wait time for loading wizzair.site



def button_clicker(button,driver,wait):
    wait.until(ec.presence_of_element_located((By.XPATH, button)))
    driver.find_element_by_xpath(button).click()





def fill_lists(href,driver):
    element = driver.find_elements_by_xpath(href)
    ellist = [value.text for value in element]
    return ellist


def click_all_offers(href,driver,wait):
    wait.until(ec.presence_of_element_located((By.XPATH, href)))
    elements = driver.find_elements_by_xpath(href)
    for elem in elements:
        elem.click()


def fill_data(object):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    wait = WebDriverWait(driver, 20)
    cheap_flight_href = 'https://www.cheapflights.co.uk/flight-search/{0}-{1}/{2}?sort=price_a'.format(
        object.get_fly_from(),
        object.get_fly_to(),
        object.get_date_from())
    # get site
    driver.get(cheap_flight_href)
    driver.maximize_window()
    try:
        # acccepting policy values
        button_clicker(value_privacy_accept,driver,wait)
    except:
        print('ELEMENT NOT FOUND')
    global dep_times_list
    global arr_times_list

    global price_list
    global durations_list
    link_list = []
    airlines_list = []
    # global stops_list
    # global// layovers_list
    # //div[@class="above-button"]

    wait
    dep_times_list = fill_lists('//*[@class="depart-time base-time"]',driver)
    arr_times_list = fill_lists('//*[@class="arrival-time base-time"]',driver)
    airlines = driver.find_elements_by_xpath('//*[@class="codeshares-airline-names"]')
    #airlines_list = [re.sub(r'[^a-zA-Z]*', '', value.text) for value in airlines]
    airlines = [value.text for value in airlines]
    for string in airlines:
        if "," in string:
            airlines_list.append("MultipleAirlines")
        else:
            string = re.sub(r"\s+",'',string)
            airlines_list.append(string)
    print(airlines_list)
    price_list = fill_lists('//*[@class="above-button"]//child::div//child::a//child::span//child::span'
                            '[@class="price-text"]',driver)
    #prices = driver.find_elements_by_xpath('//div[@class="above-button"]')
    #price_list = [re.sub(r'[^0-9]','', price.text)[0:3] for price in prices]

    #print(price_list)
    click_all_offers('//*[@class="flights"]',driver,wait)
    durations_list = fill_lists('//*[@class="duration"]',driver)
    links = driver.find_elements_by_xpath('//*[@class="booking-link " and @aria-label="View Deal"]')
    for link in links:
        link_list.append(link.get_attribute('href'))
    dataset = pd.DataFrame()
    # dataset.columns(['dTime', 'aTime','airline','price','duration','deep_link'])
    for i in range(len(dep_times_list)):
        try:
            dataset.loc[i, 'dTime'] = dep_times_list[i]
        except:
            pass
        try:
            dataset.loc[i, 'aTime'] = arr_times_list[i]
        except:
            pass
        try:
            dataset.loc[i, 'airline'] = airlines_list[i]
        except:
            pass
        try:
            dataset.loc[i, 'price'] = price_list[i]
        except:
            pass
        try:
            dataset.loc[i, 'duration'] = durations_list[i]
        except:
            pass
        try:
            dataset.loc[i, 'deep_link'] = link_list[i]
        except:
            pass
    return dataset
