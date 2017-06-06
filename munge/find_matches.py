'''
This script finds the AirBNB property with a title most similar to a VRBO or Homeaway property.
'''

import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz, process
import googlemaps
import os
import geopy.distance

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

def get_homeaway(cols):
    homeaway = pd.read_pickle('../data/homeaway.pkl')
    homeaway['service'] = 'Homeaway'
    df_h = homeaway[['latitude', 'longitude', 'service', 'homeaway_property_id', 'title']]
    df_h.columns = cols
    return df_h

def get_vrbo(cols):
    vrbo = pd.read_pickle('../data/vrbo.pkl')
    vrbo['service'] = 'VRBO'
    df_v = vrbo[['lat', 'lon', 'service', 'listingNumber', 'headline']]
    df_v.columns = cols
    return df_v

def combine_data():
    cols = ['lat', 'lon', 'service', 'prop_id', 'title']
    df_h =  get_homeaway(cols)
    df_v = get_vrbo(cols)
    df_all = pd.concat([df_h, df_v], axis=0)
    df_all.drop_duplicates('title', inplace=True)
    return df_all

def get_matches(df, df_a):
    print('Searching for matches...')
    matches = []
    for i, row in df.iterrows():
        title, score, idx = process.extractOne(row['title'], df_a['title'], scorer=fuzz.ratio)
        if score >= 80:
            airbnb_coords, other_coords = (df_a.loc[idx, 'latitude'], df_a.loc[idx, 'longitude']), (row['lat'], row['lon'])
            distance = geopy.distance.vincenty(airbnb_coords, other_coords).km
            if distance <= .5:
                matches.append([score, distance, row['service'], row['prop_id'], row['title'], df_a.loc[idx, 'airbnb_property_id'], df_a.loc[idx, 'title'], df_a.loc[idx, 'room_type']])
    matches = pd.DataFrame(matches, columns=['score', 'distance', 'service', 'id_other', 'title_other', 'airbnb_property_id', 'title_airbnb', 'room_type'])
    matches.sort_values('score', inplace=True, ascending=False)
    matches.drop_duplicates('airbnb_property_id', inplace=True)
    return matches

if __name__ == '__main__':
    df = combine_data()
    df_a = pd.read_pickle('../data/airbnb_titles.pkl')
    matches = get_matches(df, df_a)
    matches.to_pickle('../data/matches.pkl')
    matches.to_csv('../data/matches.csv')
