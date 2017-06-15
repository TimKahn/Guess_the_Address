from sklearn.model_selection import train_test_split
import pandas as pd

def get_split():
    df = pd.read_csv('../data/featurized_data.csv')
    print(df.info())
    identifiers = df.loc[:, ['attom_id', 'airbnb_property_id', 'airbnb_host_id', 'first_name', 'first_name2', 'title']]
    df = df.drop(['attom_id', 'airbnb_property_id', 'airbnb_host_id', 'first_name', 'first_name2', 'title'], axis=1)
    y = df.pop('MATCH').values
    df = df.values
    X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=.1, random_state=42, stratify=y)
    return X_train, X_test, y_train, y_test

if __name__ == '__main__':
    get_split()
