from sklearn.model_selection import train_test_split
import pandas as pd

def get_xy(filepath = '../data/featurized_500.csv'):
    df = pd.read_csv(filepath)
    # print(df.info())
    identifiers = df.loc[:, ['attom_id', 'airbnb_property_id', 'airbnb_host_id', 'first_name', 'first_name2', 'title']]
    df = df.drop(['attom_id', 'airbnb_property_id', 'airbnb_host_id', 'first_name', 'first_name2', 'title'], axis=1)
    y = df.pop('MATCH').values
    X = df.values
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.01, random_state=42, stratify=y)
    # return X_train, X_test, y_train, y_test
    return X, y

if __name__ == '__main__':
    get_xy()
