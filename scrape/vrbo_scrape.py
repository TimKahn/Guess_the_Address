'''
This script scrapes Denver VRBO listings, uses googlemaps API reverse geocoding to find their addresses,
and saves the results both as a .csv and as a pickle.
'''

import requests
import os
import json
import pandas as pd
from pprint import pprint
import googlemaps
import string
import re

gmaps = googlemaps.Client(key=os.environ['GMAPS_GEOLOCATOR'])

def get_url(page_num):
    parameters = dict(
    sw_lat = '39.614431',
    sw_long = '-105.109927',
    ne_lat = '39.91424689999999',
    ne_long = '-104.6002959',
    page = page_num,
    region = '2332'
    )

    url = "https://www.vrbo.com/ajax/map/results/vacation-rentals/@{sw_lat},{sw_long},{ne_lat},{ne_long},12z?swLat={sw_lat}&swLong={sw_long}&neLat={ne_lat}&neLong={ne_long}&zoom=12&page={page}&region={region}&searchTermContext=9b810827-b5cb-4e59-a1f0-553027e04694&searchTermUuid=9b810827-b5cb-4e59-a1f0-553027e04694&sleeps=1-plus&_=1496211019307".format(**parameters)

    '''****************** TEST URLs -- the following were used to develop this function.  They are not used in production. ********************
    url1 = 'https://www.vrbo.com/ajax/map/results/vacation-rentals/@39.65237457610901,-105.04965595142579,39.826878836475025,-104.93086627857423,12z?swLat=39.65237457610901&swLong=-105.04965595142579&neLat=39.826878836475025&neLong=-104.93086627857423&zoom=12&page=1&region=2332&searchTermContext=9b810827-b5cb-4e59-a1f0-553027e04694&searchTermUuid=9b810827-b5cb-4e59-a1f0-553027e04694&sleeps=1-plus&_=1496211019307'

    url2 = 'https://www.vrbo.com/ajax/map/results/vacation-rentals/@39.69280593436666,-105.01515201465821,39.78652608215945,-104.95575717823243,13z?swLat=39.69280593436666&swLong=-105.01515201465821&neLat=39.78652608215945&neLong=-104.95575717823243&zoom=13&page=2&region=2332&searchTermContext=9b810827-b5cb-4e59-a1f0-553027e04694&searchTermUuid=9b810827-b5cb-4e59-a1f0-553027e04694&sleeps=1-plus&_=1496510365866'

    url3 = 'https://www.vrbo.com/ajax/map/results/vacation-rentals/@,,,,z?page=2&region=2332&searchTermContext=9b810827-b5cb-4e59-a1f0-553027e04694&searchTermUuid=9b810827-b5cb-4e59-a1f0-553027e04694&sleeps=1-plus&_=1496510660438'

    ************************'''

    return url

def get_data(url):
    raw = requests.get(url).text
    data = json.loads(raw)
    return data['results']['hits']

def get_street_address(split_address):
    for elem in split_address:
        street_number = re.sub(r'[^\w\s]', '', elem.split()[0])
        if street_number.isnumeric():
            return elem
        else:
            continue

def reverse_geo(lat, lon):
    print(lat, lon)
    result = gmaps.reverse_geocode((lat, lon))[0]
    full_address = result['formatted_address']
    split_address = full_address.split(',')
    street_address = get_street_address(split_address)
    zipcode = split_address[-2].split()[-1]
    gmaps_place_id = result['place_id']
    return full_address, street_address, zipcode, gmaps_place_id

def get_properties(url):
    properties = []
    for prop in get_data(url):
        geo = prop['geoCode']
        if geo['exact'] == True:
            lat, lon = geo['latitude'], geo['longitude']
            try:
                full_address, street_address, zipcode, gmaps_place_id = reverse_geo(lat, lon)
            except:
                continue
            properties.append([int(prop['listingNumber']), prop['headline'].strip(), full_address, street_address, zipcode, gmaps_place_id, lat, lon])
    return properties

def scrape_all():
    all_properties = []
    i = 1
    while i <= 10:
        try:
            print('Attempting page {}'.format(i))
            url = get_url(i)
            all_properties.extend(get_properties(url))
            i += 1
        except:
            print('Page {} scrape failed.'.format(i))
            break
    return pd.DataFrame(all_properties, columns = ['listingNumber', 'headline', 'full address', 'street_address', 'zipcode', 'gmaps_place_id', 'lat', 'lon'])

if __name__ == '__main__':
    all_results = scrape_all()
    # all_results.to_pickle('../data/vrbo.pkl')
    all_results.to_csv('../data/vrbo.csv')
