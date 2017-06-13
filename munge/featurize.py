import pandas as pd
import geopy.distance

'''FEATURES:
lat_offset: Difference in latitude (AirBNB minus Tax Assessor)
lon_offset: Difference in longitude (AirBNB minus Tax Assessor)
neighbor_count: Number of 'neighbors' in radius
Air Conditioning
Heating
Fireplace
Pets, elevator, pool, gym
Similarity scores of AirBNB Host Name(s) and First Name on Deed etc. (each score is different predictor)
Bedrooms on AirBNB listing
Bedrooms on AirBNB listing - Bedrooms in Assessor Data
Bathrooms on AirBNB listing
Bathrooms on AirBNB listing - Bathrooms in Assessor Data
Swimming pool on AirBNB listing
Swimming pool in tax assessor data
Has unit number
'''

def get_features(df):
    featurized_df = pd.DataFrame([])
    featurized_df['attom_id'] = df.loc[:, '[ATTOM ID]']
    featurized_df['airbnb_property_id'] = df.loc[:, 'airbnb_property_id']
    featurized_df['airbnb_host_id'] = df.loc[:, 'airbnb_host_id']
    featurized_df['first_name'] = df.loc[:, 'first_name']
    featurized_df['first_name2'] = df.loc[:, 'first_name2']
    featurized_df['lat_offset'] = df.loc[:, 'latitude'] - df.loc[:, 'PropertyLatitude']
    featurized_df['lon_offset'] = df.loc[:, 'longitude'] - df.loc[:, 'PropertyLongitude']
    featurized_df['neighbor_count'] = df.loc[:, 'neighbor_count']
    return featurized_df

if __name__ == '__main__':
    df = pd.read_csv('../data/merged.csv')
    featurized_df = get_features(df)
