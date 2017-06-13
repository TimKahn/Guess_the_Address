import pandas as pd

'''FEATURES:
Number of 'neighbors' in radius
Has unit number
Air Conditioning
Heating
Fireplace
Pets, elevator, pool, gym
Similarity scores of AirBNB Host Name(s) and First Name on Deed etc. (each score is different predictor)
Bedrooms on AirBNB listing
Bedrooms on AirBNB listing - Bedrooms in Assessor Data
Bathrooms on AirBNB listing
Bathrooms on AirBNB listing - Bathrooms in Assessor Data
Difference in latitude (AirBNB minus Tax Assessor)
Difference in longitude (AirBNB minus Tax Assessor)
Swimming pool on AirBNB listing
Swimming pool in tax assessor data
'''

def get_features(df):
    featurized_df = pd.DataFrame([])
    featurized_df['attom_id'] = df['[ATTOM ID]']
    featurized_df['airbnb_property_id'] = df['airbnb_property_id']
    featurized_df['airbnb_host_id'] = df['airbnb_host_id']
    featurized_df['first_name'] = df['first_name']
    featurized_df['first_name2'] = df['first_name2']

if __name__ == '__main__':
    df = pd.read_csv('../data/merged.csv')
