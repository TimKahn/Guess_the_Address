#Note: pad latitude by .005, longitude by .0065

import pandas as pd
import geopy.distance

def distance(lat, lon, df):
    pass

def find_nearby(match, df_zip):
    lat_pad = .005
    lon_pad = .0065
    lat, lon = match['latitude'], match['longitude']
    lat_max, lat_min = lat + lat_pad, lat - lad_pad
    lon_max, lon_min = lon + lon_pad, lon - lon_pad
    df_near = df_zip.query('lat_min < PropertyLatitude < lat_max')
    return df_near

if __name__ == '__main__':
    matches = pd.read_csv('../data/matches_geo.csv')
    df = pd.read_csv('../data/tax_assessor_denver.csv')
    df_zip = df[df['PropertyAddressZIP'] == 80209]
    df_near = find_nearby(matches.loc[0], df_zip)
