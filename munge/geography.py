import pandas as pd
import os
import googlemaps
import geopy.distance
import re
from time import sleep

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
    sleep(.02)
    result = gmaps.reverse_geocode((lat, lon))[0]
    full_address = result['formatted_address']
    split_address = full_address.split(',')
    street_address = get_street_address(split_address)
    zipcode = split_address[-2].split()[-1]
    gmaps_place_id = result['place_id']
    return full_address, street_address, zipcode, gmaps_place_id

def get_location(df):
    try:
        df['full_address'], df['street_address'], df['zipcode'], df['gmaps_place_id'] = reverse_geo(df['true_latitude'], df['true_longitude'])
    except:
        df['full_address'], df['street_address'], df['zipcode'], df['gmaps_place_id'] = '', '', 0, ''
    # df['lat_diff'] = df['true_latitude'] - df['latitude']
    # df['lon_diff'] = df['true_longitude'] - df['longitude']
    df['listing_distance'] = geopy.distance.vincenty((df['true_latitude'], df['true_longitude']), (df['latitude'], df['longitude'])).km
    # df['distance'] = 0 #distance of the listing from itself.  Comparison properties will show the distance from the listing to the comp address.
    return df

if __name__ == '__main__':
    df = pd.read_csv('../data/matches.csv')
    matches = df.apply(get_location, axis=1)
    matches.drop_duplicates('gmaps_place_id', inplace=True)
    matches = matches[pd.notnull(matches['street_address'])]
    matches.to_csv('../data/matches_geo.csv')
