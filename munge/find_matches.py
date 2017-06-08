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
    homeaway = pd.read_csv('../data/homeaway_denver.csv')[['latitude', 'longitude', 'homeaway_property_id', 'title']]
    homeaway['crosslisted_on'] = 'Homeaway'
    homeaway.columns = cols
    return homeaway

def get_vrbo(cols):
    vrbo = pd.read_csv('../data/vrbo.csv')[['lat', 'lon', 'listingNumber', 'headline']]
    vrbo['crosslisted_on'] = 'VRBO'
    vrbo.columns = cols
    return vrbo

def combine_data():
    cols = ['true_latitude', 'true_longitude',  'prop_id_crosslist', 'title_crosslist', 'crosslisted_on']
    df_h =  get_homeaway(cols)
    df_v = get_vrbo(cols)
    df_all = pd.concat([df_h, df_v], axis=0)
    df_all.drop_duplicates('title_crosslist', inplace=True)
    df_all = df_all[pd.notnull(df_all['title_crosslist'])]
    df_all.reset_index(drop=True)
    return df_all

def get_airbnb():
    df_a = pd.read_csv('../data/airbnb_denver.csv')
    df_a.drop_duplicates('airbnb_property_id', inplace=True)
    df_a = df_a[pd.notnull(df_a['title'])]
    df_a.reset_index(drop=True)
    return df_a

def fuzzy_match(title_crosslist, titles_airbnb):
    try:
        title, score, idx = process.extractOne(title_crosslist, titles_airbnb, scorer=fuzz.ratio, score_cutoff=50)
        return idx, score
    except:
        print('Comparison Failed on {}'.format(title_crosslist))
        return None, 0

def process_data(df_crosslist, df_a):
    df_crosslist.sort_values('match_score', inplace=True, ascending=False)
    df_crosslist.drop_duplicates('airbnb_property_id', inplace=True)
    df_crosslist = df_crosslist[pd.notnull(df_crosslist['airbnb_property_id'])]
    df_crosslist = df_crosslist[df_crosslist['airbnb_property_id'] != 'bad match']
    return df_crosslist.merge(df_a, on='airbnb_property_id', how='inner')

def find_matches():
    df_crosslist = combine_data()
    df_a = get_airbnb()
    titles_airbnb = df_a['title']
    idx_list = []
    score_list = []
    for i, row in df_crosslist.iterrows():
        idx, score = fuzzy_match(row['title_crosslist'], titles_airbnb)
        if idx:
            idx_list.append(df_a.loc[idx, 'airbnb_property_id'])
        else:
            idx_list.append('bad match')
        score_list.append(score)
    df_crosslist['airbnb_property_id'] = idx_list
    df_crosslist['match_score'] = score_list
    df_a.to_pickle('../data/df_a.pkl')
    df_crosslist.to_pickle('../data/df_crosslist.pkl')
    return

if __name__ == '__main__':
    # find_matches()
    df_a = pd.read_pickle('../data/df_a.pkl')
    df_crosslist = pd.read_pickle('../data/df_crosslist.pkl')
    matches = process_data(df_crosslist, df_a)
    matches.to_csv('../data/matches.csv')
