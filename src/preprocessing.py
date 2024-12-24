import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from pandas.api.types import is_numeric_dtype


df = pd.read_csv("data\\raw data\\spotify_tracks.csv")

df = df[df['language'] == 'English'].reset_index(drop=True)
df = df.drop_duplicates(subset=['track_name'], keep='last')

#Replace -1 with NaN value
df.replace(-1, np.nan, inplace=True)

# Impute numerical features with mean
numerical_features = ['acousticness', 'tempo', 'popularity', 'danceability', 'energy','liveness','key','loudness','speechiness','time_signature','valence','instrumentalness']  
for feature in numerical_features:
    mean_value = df[feature].mean()
    df[feature] = df[feature].fillna(mean_value)

# Impute categorical features with mode or 'Unknown'
categorical_features = ['language', 'mode','track_id','track_name','artist_name','year','artwork_url','album_name','duration_ms','track_url']  
for feature in categorical_features:
    mode_value = df[feature].mode()[0]
    df[feature] = df[feature].fillna(mode_value)

# Initialize the scaler
scaler = MinMaxScaler()

# Normalize numerical features
df[numerical_features] = scaler.fit_transform(df[numerical_features])

# Create 'party_score' feature
df['party_score'] = df['danceability'] * df['valence'] 
df['dance_score'] = df['energy'] * df['tempo']
# Confirm no missing values remain
print(df.isnull().sum().sum())  # Should output 0

# Display the first few rows of the processed DataFrame
print(df.head())
print(df.info())

# Save the preprocessed DataFrame to a new CSV file
df.to_csv('data\\raw data\\processed\\spotify_tracks_preprocessed.csv', index=False)