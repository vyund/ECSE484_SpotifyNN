import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow import feature_column

from plot import plot_acc, plot_loss
import matplotlib.pyplot as plt
import seaborn as sns

SEED = 12345
tf.random.set_seed(SEED)

data_dir = './data/data_7genres.csv'

num_classes = 7

dataframe = pd.read_csv(data_dir)
print('{} samples loaded...'.format(len(dataframe)))
dataframe = dataframe.drop_duplicates(subset='tid', keep=False)
print('{} samples after removing duplicates...'.format(len(dataframe)))
features = dataframe.drop('tid', axis=1).astype('float32')
labels = features.pop('label')

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
#keras.utils.plot_model(model, './model.png', show_shapes=True)
#model.summary()

lr = 0.0001
optimizer = tf.keras.optimizers.Adam(learning_rate=lr)

model.compile(optimizer=optimizer, loss=tf.keras.losses.SparseCategoricalCrossentropy(), metrics=['accuracy'])

history = model.fit(x_train, y_train, batch_size=32, epochs=500, validation_split=0.2)

plot_acc(history, 'genre')
plot_loss(history, 'genre')

test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)
print('\nTest accuracy: {}'.format(test_acc))

preds = model.predict(x_test)
preds = tf.argmax(preds, axis=-1)
confusion = tf.math.confusion_matrix(y_test, preds, num_classes=num_classes)

classes = ['jazz', 'classical', 'indie', 'country', 'rock', 'hip-hop', 'edm']

plt.figure(figsize=(8,6))
sns.heatmap(confusion, xticklabels=classes, yticklabels=classes, annot=True)
plt.xlabel('Pred')
plt.ylabel('True')
plt.savefig('./plots/model_cm_genre.png')