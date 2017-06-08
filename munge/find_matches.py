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
    df_all.reset_index()
    return df_all

def get_airbnb():
    df_a = pd.read_csv('../data/airbnb_denver.csv')
    df_a.drop_duplicates('title', inplace=True)
    df_a = df_a[pd.notnull(df_a['title'])]
    return df_a

def fuzzy_match(title_crosslist, titles_airbnb):
    try:
        title_crosslist, score, idx = process.extractOne(title_crosslist, titles_airbnb, scorer=fuzz.ratio, score_cutoff=50)
        return idx, score
    except:
        print('Comparison Failed on {}'.format(title_crosslist))
        return None, 0

def process_data(df_crosslist, df_a):
    df_a.sort_values('score', inplace=True, ascending=False)
    df_a = df_a[pd.notnull(df_a['idx'])]
    df_a.drop_duplicates('idx', inplace=True)
    index_list = df_a['idx']
    df_crosslist = df_crosslist.loc[index_list, :]
    return index_list, df_a, df_crosslist

def find_matches():
    df_crosslist = combine_data()
    df_a = get_airbnb()
    titles = df_crosslist['title_crosslist']
    idx_list = []
    score_list = []
    for i, row in df_a.iterrows():
        idx, score = fuzzy_match(row['title'], titles)
        idx_list.append(idx)
        score_list.append(score)
    df_a['idx'] = idx_list
    df_a['score'] = score_list
    df_a.to_pickle('../data/df_a.pkl')
    df_crosslist.to_pickle('../data/df_crosslist.pkl')
    return

if __name__ == '__main__':
    # find_matches()
    df_a = pd.read_pickle('../data/df_a.pkl')
    df_crosslist = pd.read_pickle('../data/df_crosslist.pkl')
    index_list, df_a, df_crosslist = process_data(df_crosslist, df_a)
    # matches.to_csv('../data/matches.csv')
