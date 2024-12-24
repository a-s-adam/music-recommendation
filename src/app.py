from flask import Flask, jsonify, request, render_template
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

app = Flask(__name__)

# Load and preprocess data
df = pd.read_csv('data\\raw data\\processed\\spotify_tracks_preprocessed.csv')

required_features = ['energy', 'tempo', 'danceability', 'acousticness', 'loudness', 'valence']
scaler = MinMaxScaler()
feature_matrix = scaler.fit_transform(df[required_features])
similarity_matrix = cosine_similarity(feature_matrix)

@app.route('/recommend_ui', methods=['GET'])
def recommend_ui():
    track_name = request.args.get('track_name')
    top_n = int(request.args.get('top_n', 5))  # Default to 5 recommendations

    if not track_name:
        return render_template("index.html", recommendations=None, track_names=df['track_name'].tolist())

    if track_name not in df['track_name'].values:
        return render_template("index.html", recommendations=None, track_names=df['track_name'].tolist(),
                               error=f"Track '{track_name}' not found.")

    idx = df.index[df['track_name'] == track_name].tolist()[0]
    similarity_scores = list(enumerate(similarity_matrix[idx]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    # Retrieve top N similar tracks excluding the input track
    seen_tracks = set()
    recommendations = []
    for i in similarity_scores[1:]:
        track = df['track_name'].iloc[i[0]]
        artist = df['artist_name'].iloc[i[0]]
        if track != track_name and track not in seen_tracks:
            recommendations.append({"track_name": track, "artist_name": artist})
            seen_tracks.add(track)
        if len(recommendations) >= top_n:
            break

    return render_template("index.html", recommendations=recommendations, track_name=track_name,
                           track_names=df['track_name'].tolist())

@app.route('/')
def home():
    return render_template("index.html", track_names=df['track_name'].tolist())


if __name__ == '__main__':
    app.run(debug=True)
