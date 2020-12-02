import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

from plot import plot_acc, plot_loss, plot_cm

# For experiment reproducibility 
SEED = 12345
tf.random.set_seed(SEED)

# To get class labels for each experiment (Note: 4 is for mood experiment)
class_dict = {
    3: ['classical', 'rock', 'edm'],
    4: ['study', 'road-trip', 'workout', 'party'],
    5: ['jazz', 'classical', 'rock', 'hip-hop', 'edm'],
    7: ['jazz', 'classical', 'indie', 'country', 'rock', 'hip-hop', 'edm']
}

# Load the CSV file into Pandas dataframe of features and labels
def load_data(data_path, verbose=True):
    dataframe = pd.read_csv(data_path)
    dataframe = dataframe.drop_duplicates(subset='tid', keep=False)
    if verbose:
        print('{} samples loaded...'.format(len(dataframe)))
        print('{} samples after removing duplicates...'.format(len(dataframe)))
    features = dataframe.drop('tid', axis=1).astype('float32')
    labels = features.pop('label')

    return features, labels

# Train model with provided hyperparameters and test on held-out set
def model(features, labels, experiment, lr=0.0001, batch_size=32, epochs=500, verbose=True):

    x_train, x_test, y_train, y_test = train_test_split(features, labels, test_size=0.20, stratify=labels, random_state=SEED)

    leaky_relu = tf.keras.layers.LeakyReLU(alpha=0.1)

    input_layer = keras.Input(shape=(11,))
    x = layers.Dense(128, activation=leaky_relu)(input_layer)
    x = layers.Dense(64, activation=leaky_relu)(x)
    x = layers.Dropout(0.2)(x)
    x = layers.Dense(64, activation=leaky_relu)(x)
    x = layers.Dense(32, activation=leaky_relu)(x)
    x = layers.LayerNormalization()(x)
    x = layers.Dense(num_classes)(x)
    output_layer = layers.Softmax()(x)

    model = keras.Model(inputs=input_layer, outputs=output_layer, name='spotify_nn')
    if verbose:
        #keras.utils.plot_model(model, './model_diagram.png', show_shapes=True)
        model.summary()

    optimizer = tf.keras.optimizers.Adam(learning_rate=lr)

    model.compile(optimizer=optimizer, loss=tf.keras.losses.SparseCategoricalCrossentropy(), metrics=['accuracy'])

    history = model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_split=0.2)

    plot_acc(history, num_classes, experiment)
    plot_loss(history, num_classes, experiment)

    test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)
    if verbose:
        print('\nTest accuracy: {}'.format(test_acc))

    preds = model.predict(x_test)
    preds = tf.argmax(preds, axis=-1)
    confusion_matrix = tf.math.confusion_matrix(y_test, preds, num_classes=num_classes)

    plot_cm(confusion_matrix, classes, num_classes, experiment)

if __name__ == '__main__':
    experiment = 'mood'
    num_classes = 4
    classes = class_dict[num_classes]

    data_dir = './data/data_{}{}.csv'.format(num_classes, experiment)

    features, labels = load_data(data_dir)
    model(features, labels, experiment, lr=0.0001, batch_size=32, epochs=500)
