import pandas as pd
import os
import googlemaps
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

def mapper(df):
    try:
        df['full_address'], df['street_address'], df['zipcode'], df['gmaps_place_id'] = reverse_geo(df['latitude'], df['longitude'])
    except:
        df['full_address'], df['street_address'], df['zipcode'], df['gmaps_place_id'] = '', '', 0, ''
    return df

if __name__ == '__main__':
    df = pd.read_csv('../data/homeaway_denver.csv')[['homeaway_property_id', 'latitude', 'longitude', 'title', 'geocode_exact']]
    df = df[df.geocode_exact == True]
    df = df.apply(mapper, axis=1)
    df.to_pickle('../data/homeaway.pkl')
