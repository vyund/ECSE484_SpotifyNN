# SpotifyNN
## Classifying Spotify song genres through use of neural networks.

### Background:
Song information that can be retrieved through Spotify’s API contain song attributes (acousticness, loudness, energy, etc.) which can then be represented as a feature vector. Spotify provides playlists based by genre or even mood. Given these song attributes, I hypothesize that a trained neural network should be able to accurately classify the song’s genre, provided that the genres are not too closely related.

As an extension to this project, I also repeated my experiment using Spotify playlist for particular “moods”, such as study music, or workout music.

### Requirements:
* numpy 1.18.5
* matplotlib 3.1.3
* pandas 1.1.4
* seaborn 0.9.0
* scikit-learn 0.21.3
* tensorflow 2.3.1
* spotipy 2.16.1

### Usage:
#### _data_genre.py_
Extracts 11 song features from pre-determined Spotify playlists using Spotify’s API. Features per song are strung out horizontally and stored as a row in the resulting CSV file. Samples are encoded with numeric values, which correspond to the genre of the song. Samples also include the track ID (*tid*), which can be used to identify the song and retrieve other relevant song information if needed. Note that songs are added in a manner such that genres are all grouped together. These samples are shuffled before being split into training and test sets.

#### _data_mood.py_
Performs functionality of *data_genre.py*, but for Spotify’s “mood” playlists.

#### _model.py_
Loads specified CSV file into a Pandas Dataframe. Then, splits into training and test sets and passed through TensorFlow model. 20% of the dataset is used as the held-out test set, and 20% of the training set is used as validation. Model architecture was found experimentally to yield best performance per class size experiment. Hyperparameters that were used in experiments are provided by default. 

#### _plot.py_
Provides helper functions to plot model metrics, such as training/validation accuracy and loss, as well as resulting confusion matrix.

### Model Architecture:
![Model Architecture](/model_diagram.png)

### Results:
#### 3-class Genre Experiment
* 89.45% test accuracy

![3-Genre Model Confusion Matrix](/plots/model_cm_3genres.png)

#### 5-class Genre Experiment
* 83.49% test accuracy

![5-Genre Model Confusion Matrix](/plots/model_cm_5genres.png)

#### 7-class Genre Experiment
* 67.90% test accuracy

![7-Genre Model Confusion Matrix](/plots/model_cm_7genres.png)

#### 4-class "Mood" Experiment
* 71.37% test accuracy

![4-Mood Model Confusion Matrix](/plots/model_cm_4moods.png)

### Discussion:
Results are promising, and show that it is possible for a neural network to be able to classify song genre based on its attribute. While the test accuracy for the experiments are relatively low, the confusion matrices show that errors in classification are related to the intrinsic similarities of certain genres of music. For example, the similar properties of indie, country, or rock music. Further experiments will be done to attempt to increase performance, but given the current dataset size, I did not want to overfit the model.
