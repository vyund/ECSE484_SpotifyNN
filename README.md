# ECSE484_SpotifyNN
## Classifying Spotify song genres through use of neural networks.

### Background:
Song information that can be retrieved through Spotify’s API contain song attributes (acousticness, loudness, energy, etc.) which can then be represented as a feature vector. Spotify provides playlists based by genre or even mood. Given these song attributes, I hypothesize that a trained neural network should be able to accurately classify the song’s genre, provided that the genres are not too closely related.

As an extension to this project, I also repeated my experiment using Spotify playlist for particular “moods”, such as study music, or workout music.

### Requirements:
numpy 1.18.5
matplotlib 3.1.3
pandas 1.1.4
seaborn 0.9.0
scikit-learn 0.21.3
tensorflow 2.3.1
spotipy 2.16.1

### Usage:
#### data_genre.py
Extracts song features from pre-determined Spotify playlists using Spotify’s API. Features per song are strung out horizontally and stored as a row in the resulting CSV file. Samples are encoded with numeric values, which correspond to the genre of the song. Samples also include the track ID (tid), which can be used to identify the song and retrieve other relevant song information if needed. Note that songs are added in a manner such that genres are all grouped together. During training/testing, these samples are shuffled.

#### data_mood.py
Performs functionality of data_genre.py, but for Spotify’s “mood” playlists.

#### model.py
Loads specified CSV file into a Pandas Dataframe. Then, splits into training and test sets and passed through TensorFlow model. Model architecture was found experimentally to yield best performance per class size experiment. Hyperparameters that were used in experiments are provided by default.  
