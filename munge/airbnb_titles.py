'''
Pickles airbnb property id and title for text comparison to VBRO/Homeaway.
Adds googlemaps place id, which is likely incorrect, but within 400m of true address.
'''

import pandas as pd
import googlemaps
import os

gmaps = googlemaps.Client(key=os.environ['GMAPS_GEOLOCATOR'])

def reverse_geo(row):
    lat, lon = row['latitude'], row['longitude']
    print(lat, lon)
    return gmaps.reverse_geocode((lat, lon))[0]['place_id']

if __name__ == '__main__':
    df_a = pd.DataFrame()
    df_a[['prop_id', 'title', 'latitude', 'longitude']] = pd.read_csv('../data/airbnb_denver.csv')[['airbnb_property_id', 'title', 'latitude', 'longitude']]
    #df_a['gmaps_place_id'] = df_a.apply(reverse_geo, axis=1)
    df_a['gmaps_place_id'] = 0
    df_a['service'] = 'AirBNB'
    df_a = df_a[['gmaps_place_id', 'service', 'prop_id', 'title']]
    df_a.dropna(axis=0, how='any', inplace=True)
    df_a.drop_duplicates('title', inplace=True)
    df_a.to_pickle('../data/airbnb_titles.pkl')
