'''
Pickles airbnb property id and title for text comparison to VBRO/Homeaway.
I opted to skip reverse geocoding at this step, but left functionality available, just in case.
'''

import pandas as pd
import googlemaps
import os

gmaps = googlemaps.Client(key=os.environ['GMAPS_GEOLOCATOR'])

def reverse_geo(row):
    lat, lon = row['latitude'], row['longitude']
    print(lat, lon)
    try:
        place_id = gmaps.reverse_geocode((lat, lon))[0]['place_id']
    except:
        print('{}, {} reverse geocode failed'.format(lat, lon))
        place_id = None
    return place_id

if __name__ == '__main__':
    df = pd.DataFrame()
    df = pd.read_csv('../data/airbnb_denver.csv')[['airbnb_property_id', 'title', 'latitude', 'longitude', 'room_type']]
    # df['gmaps_place_id'] = df.apply(reverse_geo, axis=1)
    df['service'] = 'AirBNB'
    df.dropna(axis=0, how='any', inplace=True)
    df.drop_duplicates('title', inplace=True)
    df.to_pickle('../data/airbnb_titles.pkl')
