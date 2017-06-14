import split
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

if __name__ == '__main__':
    X_train, X_test, y_train, y_test = split.get_split()
    rfc = RandomForestClassifier(n_estimators = 100, random_state=42, max_features=None, class_weight={0:1, 1:2}, n_jobs=-1)
    print(cross_val_score(rfc, X_train, y_train, cv=5, scoring='recall', n_jobs=-1))
