#Note: pad latitude by .005, longitude by .0065

import pandas as pd
import geopy.distance

def get_distance(row, lat, lon):
    '''
    Takes a row from attom data and a fixed lat & lon; returns the distance.
    '''
    return geopy.distance.vincenty((lat, lon), (row['PropertyLatitude'], row['PropertyLongitude'])).km

def find_nearby(match, df_zip):
    lat_pad = .005
    lon_pad = .0065
    lat, lon = match['latitude'], match['longitude']
    lat_max = lat + lat_pad
    lat_min = lat - lat_pad
    lon_max = lon + lon_pad
    lon_min = lon - lon_pad
    df_near = df_zip[(df_zip['PropertyLatitude'] > lat_min) & (df_zip['PropertyLatitude'] < lat_max) & (df_zip['PropertyLongitude'] > lon_min) & (df_zip['PropertyLongitude'] < lon_max)]
    return df_near

def find_in_radius(match, df_near):
    radius = .5
    lon = match['longitude']
    df_near['distance'] = df_near.apply(lambda row: get_distance(row, match['latitude'], match['longitude']), axis=1)
    df_near['true_distance'] = df_near.apply(lambda row: get_distance(row, match['true_latitude'], match['true_longitude']), axis=1)
    df_radius = df_near[df_near['distance'] <= radius]
    find_true_match(match, df_radius)
    return df_radius

def find_true_match(match, df_radius):
    print('\n****ACTUAL: {}'.format(match['street_address']))
    df = df_radius[df_radius['true_distance'] < .002]
    print('****MATCHES:\n{}'.format(df['PropertyAddressFull']))
    return

def find_all(matches_df, tax_df):
    for z in matches_df.zipcode.unique():
        matches_zip = matches_df[matches_df['zipcode'] == z]
        df_zip = tax_df[tax_df['PropertyAddressZIP'] == z]
        for i, match in matches_zip.iterrows():
            df_near = find_nearby(match, df_zip)
            df_radius = find_in_radius(match, df_near)
            find_true_match(match, df_radius)
    return

if __name__ == '__main__':
    matches_df = pd.read_csv('../data/matches_geo.csv')
    tax_df = pd.read_csv('../data/tax_assessor_denver.csv')
    tax_df = tax_df[tax_df['CompanyFlag'] != 'Y']
    find_all(matches_df, tax_df)
