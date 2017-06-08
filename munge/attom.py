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
    lat = match['latitude']
    lon = match['longitude']
    df_near['distance'] = df_near.apply(lambda row: get_distance(row, lat, lon), axis=1)
    df_radius = df_near[df_near['distance'] <= radius]
    return df_radius

if __name__ == '__main__':
    matches = pd.read_csv('../data/matches_geo.csv')
    df = pd.read_csv('../data/tax_assessor_denver.csv')
    df_zip = df[(df['PropertyAddressZIP'] == 80209) & (df['CompanyFlag'] != 'Y')]
    df_near = find_nearby(matches.loc[0], df_zip)
    df_radius = find_in_radius(matches.loc[0], df_near)
