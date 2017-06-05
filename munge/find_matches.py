'''
This script finds the AirBNB property with a title most similar to a VRBO or Homeaway property.
'''

import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz, process

def get_homeaway(cols):
    homeaway = pd.read_pickle('../data/homeaway.pkl')
    homeaway['service'] = 'Homeaway'
    df_h = homeaway[['gmaps_place_id', 'service', 'homeaway_property_id', 'title']]
    df_h.columns = cols
    return df_h

def get_vrbo(cols):
    vrbo = pd.read_pickle('../data/vrbo.pkl')
    vrbo['service'] = 'VRBO'
    df_v = vrbo[['gmaps_place_id', 'service', 'listingNumber', 'headline']]
    df_v.columns = cols
    return df_v

def combine_data():
    cols = ['gmaps_place_id', 'service', 'prop_id', 'title']
    df_h =  get_homeaway(cols)
    df_v = get_vrbo(cols)
    df_all = pd.concat([df_h, df_v], axis=0)
    df_all.drop_duplicates('title', inplace=True)
    return df_all

def get_matches(df, df_a):
    matches = []
    count = 0
    for i, row in df.iterrows():
        title, score, idx = process.extractOne(row['title'], df_a['title'], scorer=fuzz.ratio)
        if score >= 80:
            matches.append([score, row['service'], row['prop_id'], row['title'], df_a.loc[idx, 'prop_id'], df_a.loc[idx, 'title']])
            count +=1
            print(count)
    matches = pd.DataFrame(matches, columns=['score', 'service', 'id_other', 'title_other', 'id_airbnb', 'title_airbnb'])
    matches.sort_values('score', inplace=True, ascending=False)
    matches.drop_duplicates('id_airbnb', inplace=True)
    return matches

if __name__ == '__main__':
    df = combine_data()
    df_a = pd.read_pickle('../data/airbnb_titles.pkl')
    matches = get_matches(df, df_a)
