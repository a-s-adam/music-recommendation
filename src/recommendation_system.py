import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import random

# Load the dataset
print("Loading dataset...")
df = pd.read_csv('data\\raw data\\processed\\spotify_tracks_preprocessed.csv')
print(f"Dataset loaded with {len(df)} rows and {len(df.columns)} columns.")

# Filter for English songs
df = df[df['language'] == 'English'].reset_index(drop=True)
print(f"Filtered dataset contains {len(df)} rows.")

# Ensure 'track_name' and 'artist_name' exist in the DataFrame
if 'track_name' not in df.columns or 'artist_name' not in df.columns:
    raise ValueError("The 'track_name' or 'artist_name' column is missing from the dataset.")

# Ensure features used for similarity calculation exist
required_features = ['energy','tempo','danceability','acousticness','loudness','valence']
missing_features = [feature for feature in required_features if feature not in df.columns]
if missing_features:
    raise ValueError(f"The following required features are missing: {missing_features}")

print("Required features are present. Proceeding with similarity calculation...")

# Compute cosine similarity matrix
print("Computing cosine similarity matrix...")
feature_matrix = df[required_features]
print(f"Feature matrix shape: {feature_matrix.shape}")
similarity_matrix = cosine_similarity(feature_matrix)
print("Cosine similarity matrix computed.")

# Inspect feature matrix values
print("Sample values from feature matrix:")
print(feature_matrix.head())

# Debugging inside the get_similar_tracks function
def get_similar_tracks(track_name, top_n=5):
    print(f"Searching for track name {track_name}...")

    # Ensure track_name is a string to match dataset format
    track_name = str(track_name)

    if track_name not in df['track_name'].values:
        raise ValueError(f"Track name {track_name} not found in the dataset.")

    # Get the index of the given track name
    idx_list = df.index[df['track_name'] == track_name].tolist()
    if not idx_list:
        raise ValueError(f"Track name {track_name} not found in the dataset.")

    idx = idx_list[0]
    print(f"Found track name {track_name} by artist {df['artist_name'].iloc[idx]} at index {idx}.")
    
    # Compute similarity scores
    print(f"Computing similarity scores for track name {track_name}...")
    similarity_scores = list(enumerate(similarity_matrix[idx]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    print(f"Similarity scores computed. Top similarity scores: {similarity_scores[:10]}")  # Debug: print top scores

    # Retrieve the top N similar tracks with artist names, excluding duplicates and the input track
    seen_tracks = set()
    similar_tracks = []
    for i in similarity_scores[1:]:
        track = df['track_name'].iloc[i[0]]
        artist = df['artist_name'].iloc[i[0]]
        if track != track_name and track not in seen_tracks:
            similar_tracks.append({"track_name": track, "artist_name": artist})
            seen_tracks.add(track)
        if len(similar_tracks) >= top_n:
            break

    print(f"Top {top_n} similar tracks for track name {track_name}: {similar_tracks}")
    return similar_tracks

# # Add more features to the similarity matrix
# additional_features = ['tempo', 'popularity', 'loudness']
# for feature in additional_features:
#     if feature in df.columns:
#         required_features.append(feature)

# # Recompute similarity matrix with expanded features
# print("Recomputing similarity matrix with additional features...")
# feature_matrix = df[required_features]
# similarity_matrix = cosine_similarity(feature_matrix)
# print(f"Feature matrix shape after adding features: {feature_matrix.shape}")

# Example usage: Get a random track and its artist
try:
    random_track_idx = random.randint(0, len(df) - 1)
    random_track = df['track_name'].iloc[random_track_idx]
    random_artist = df['artist_name'].iloc[random_track_idx]
    print(f"Random track selected: '{random_track}' by {random_artist}")

    similar_tracks = get_similar_tracks(random_track)
    print("Similar tracks with artist names:")
    for track in similar_tracks:
        print(f"Track: {track['track_name']}, Artist: {track['artist_name']}")
except ValueError as e:
    print(f"Error: {e}")
