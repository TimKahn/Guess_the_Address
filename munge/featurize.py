import pandas as pd
import geopy.distance
import re

'''FEATURES:
zipcode
neighbor_count: Number of 'neighbors' in radius
lat_offset: Difference in latitude (AirBNB minus Tax Assessor)
lon_offset: Difference in longitude (AirBNB minus Tax Assessor)
fireplace_a: boolean -- airbnb indoor_fireplace == True
fireplace_t: boolean -- tax assessor Fireplace code == 1.0
beds_a: Bedrooms on AirBNB listing
bed_diff: Bedrooms on AirBNB listing minus Bedrooms in Assessor Data
baths_a: Bathrooms on AirBNB listing
bath_diff: Bathrooms on AirBNB listing minus Bathrooms in Assessor Data
name_score: Similarity scores of AirBNB Host Name(s) and First Name on Deed etc. (each score is a different predictor?)

CANDIDATES DROPPED:
pool_a: boolean -- swimming pool in airbnb listing
pool_t: boolean -- swimming pool in tax assessor data
accomodates -- all NaN
AreaBuilding -- not useful without 'accomodates' data
pets_a, elevator_a, gym_a: all boolean, from airbnb listing
unit_number_t
Air Conditioning -- not included; mostly NaN in attom, mostly True in airbnb
Heating -- not included; assume the False listings in airbnb probably still have heating (it's Denver).
Pool (tax assessor) -- 5 matches had pools per airbnb; none showed a pool in tax assessor data.
'''

def get_features(df):
    featurized_df = pd.DataFrame([])
    featurized_df['MATCH'] = df.loc[:, 'MATCH'].apply(lambda x: 1 if x == True else 0) #whether this a confirmed address match.  This will be y.
    featurized_df['attom_id'] = df.loc[:, '[ATTOM ID]']
    featurized_df['airbnb_property_id'] = df.loc[:, 'airbnb_property_id']
    featurized_df['airbnb_host_id'] = df.loc[:, 'airbnb_host_id']
    featurized_df['first_name'] = df.loc[:, 'first_name']
    featurized_df['first_name2'] = df.loc[:, 'first_name2']
    #predictors start here...
    featurized_df['zipcode'] = df.loc[:, 'zipcode']
    featurized_df['neighbor_count'] = df.loc[:, 'neighbor_count']
    featurized_df['lat_offset'] = df.loc[:, 'latitude'] - df.loc[:, 'PropertyLatitude']
    featurized_df['lon_offset'] = df.loc[:, 'longitude'] - df.loc[:, 'PropertyLongitude']
    featurized_df['fireplace_a'] = df['indoor_fireplace'].apply(lambda x: 1 if x == True else 0)
    featurized_df['fireplace_t'] = df['Fireplace'].apply(lambda x: 1 if x == 1.0 else 0)
    featurized_df['beds_a'] = df.loc[:, 'bedrooms']
    featurized_df['baths_a'] = df.loc[:, 'bathrooms']
    featurized_df['bed_diff'] = df.loc[:, 'bedrooms'] - df.loc[:, 'BedroomsCount']
    featurized_df['bath_diff'] = df.loc[:, 'bathrooms'] - df.loc[:, 'BathCount']
    featurized_df['name_score'] = df.loc[:, 'name_score']
    return featurized_df

if __name__ == '__main__':
    df = pd.read_csv('../data/merged.csv')
    featurized_df = get_features(df)
