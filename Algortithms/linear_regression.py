import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

def calculate_duration(start, end):
    start = pd.to_datetime(start, format='%H:%M')
    end = pd.to_datetime(end, format='%H:%M')
    if end < start:
        end += pd.Timedelta(days=1)  # Adjust for overnight travel
    duration = (end - start).seconds / 60  # Duration in minutes
    return duration

def minimal_cost(data,cost):
    df = pd.DataFrame(data)
    df.dropna(axis=0, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df['duration'] = df.apply(lambda row: calculate_duration(row['startTime'], row['endTime']), axis=1)
    categorical_features = ['busName', 'busFrom', 'busTo', 'acNonAc', 'busType']
    encoder = OneHotEncoder()
    encoded_features = encoder.fit_transform(df[categorical_features]).toarray()
    encoded_df = pd.DataFrame(encoded_features, columns=encoder.get_feature_names_out(categorical_features))

    features = pd.concat([encoded_df, df[['noOfSeats', 'duration']]], axis=1)
    target = df['cost']

    features.dropna(axis=0,inplace=True)

    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    predicted_costs = model.predict(features)
    df['predicted_costs'] = predicted_costs
    # recommended_buses = df[predicted_costs <= cost]

    df['cost_diff'] = np.abs(df['predicted_costs'] - cost)
    df_sorted = df.sort_values(by='cost_diff')
    recommended_buses = df_sorted.head(20)

    return recommended_buses.to_dict(orient='records')