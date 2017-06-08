#Note: pad latitude by .005, longitude by .0065

import pandas as pd
import os
import googlemaps
import geopy.distance
import re

gmaps = googlemaps.Client(key=os.environ['GMAPS_GEOLOCATOR'])

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

def get_location():
    df = pd.read_csv('../data/matches.csv')
    try:
        df['full_address'], df['street_address'], df['zipcode'], df['gmaps_place_id'] = reverse_geo(df['true_latitude'], df['true_longitude'])
    except:
        df['full_address'], df['street_address'], df['zipcode'], df['gmaps_place_id'] = '', '', 0, ''

    distance = geopy.distance.vincenty(airbnb_coords, true_coords).km
    return df

if __name__ == '__main__':
    get_location()
    # matches = matches.query("match_score >= 85 & distance <= .5 & room_type == 'Entire home/apt'")
