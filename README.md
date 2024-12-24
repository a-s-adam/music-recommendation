
https://www.kaggle.com/datasets/gauthamvijayaraj/spotify-tracks-dataset-updated-every-week/data

# Music Recommendation System

A Python-based application that provides personalized music recommendations using machine learning techniques.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Personalized Recommendations**: Suggests songs based on the chosen track & track features
- **Flask Web Interface**: Provides an interactive UI for users to receive recommendations.

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/a-s-adam/music-recommendation.git
   cd music-recommendation

## Project Structure

1. preprocessing.py : code to preprocess the data to fill "unavailable values" (-1 value) with either NaN or Unknown, depending on if it is numerical or categorical. The dataset has multiple languages, but all languages are filtered out except for English.
2. recommendation_system.py: Recommendation system that uses numerical features and compares them in a cossine matrix to produce the Top-N similar songs to a randomly selected track.
3. app.py: Flask UI code to use the system produced from recommendation_system.py