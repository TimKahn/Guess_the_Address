import pandas as pd
import geopy.distance

'''FEATURES:
zipcode
neighbor_count: Number of 'neighbors' in radius
lat_offset: Difference in latitude (AirBNB minus Tax Assessor)
lon_offset: Difference in longitude (AirBNB minus Tax Assessor)
Air Conditioning -- not included; mostly NaN in attom, mostly True in airbnb
Heating -- not included; assume the False listings in airbnb probably still have heating (it's Denver).
fireplace_a: boolean -- airbnb indoor_fireplace == True
fireplace_t: boolean -- tax assessor Fireplace code == 1.0
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
    featurized_df['MATCH'] = df.loc[:, 'MATCH']
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
    return featurized_df

if __name__ == '__main__':
    df = pd.read_csv('../data/merged.csv')
    featurized_df = get_features(df)
