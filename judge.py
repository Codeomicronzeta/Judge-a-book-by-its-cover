# -*- coding: utf-8 -*-
"""
Automatically generated by Colaboratory.
"""

# Importing required libraries
import cv2
from google.colab.patches import cv2_imshow
import os
from os import listdir
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

path = r'/content/drive/MyDrive/Dataset/Class/'

# Setting the batch size and image parameters
batch_size = 32
img_height = 180
img_width = 180

# Creating training dataset which contains 80% of the total data
train_ds = tf.keras.preprocessing.image_dataset_from_directory(
  path,
  validation_split=0.2,
  subset="training",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

# Creating Validation dataset which contains the remanining 20% of the dataset
val_ds = tf.keras.preprocessing.image_dataset_from_directory(
  path,
  validation_split=0.2,
  subset="validation",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

# Code for augmenting data with horizontal flipping and random zooming
from tensorflow.keras import layers
data_augmentation = tf.keras.Sequential(
  [
    layers.experimental.preprocessing.RandomFlip("horizontal", 
                                                 input_shape=(img_height, 
                                                              img_width,
                                                              3)),
    layers.experimental.preprocessing.RandomZoom(0.1),
  ]
)

# Setting up the CNN architecture along with data augmentation and Dropout by specifying the required parameters
from tensorflow.keras import layers
num_classes = 3

model = tf.keras.Sequential([
  data_augmentation,
  layers.experimental.preprocessing.Rescaling(1./255),
  layers.Conv2D(16, 3, activation='relu',padding='same'),
  layers.MaxPooling2D(strides = 2),
  layers.Conv2D(32, 3, activation='relu', padding = 'same'),
  layers.MaxPooling2D(strides = 2),
  layers.Conv2D(64, 3, activation='relu', padding = 'same'),
  layers.MaxPooling2D(strides = 2),
  layers.Conv2D(90, 3, activation='relu', padding = 'same'),
  layers.MaxPooling2D(strides = 2),
  layers.Flatten(),
  layers.Dropout(0.4),
  layers.Dense(128, activation='relu'),
  layers.Dense(num_classes)
])

# Setting up the loss function and optimizer
model.compile(
  optimizer='adam',
  loss=tf.losses.SparseCategoricalCrossentropy(from_logits=True),
  metrics=['accuracy'])

# Running the created CNN model
history = model.fit(
    train_ds,
    epochs=30,
    validation_data=val_ds)

class_names = train_ds.class_names

from tensorflow import keras
import matplotlib.image as mpimg

img = mpimg.imread('/content/sample_data/cover_3.jpeg')
imgplot = plt.imshow(img)

img_array = keras.preprocessing.image.img_to_array(img)
img_array = tf.image.resize(img_array,size=(180, 180))
img_array = tf.expand_dims(img_array, 0)
img_array = img_array/255.
predictions = model.predict(img_array)
score = tf.nn.softmax(predictions[0])

print(f"Judging by its cover this book is likely to be an {class_names[np.argmax(score)]} read, with a {np.max(score)*100:.2f}% confidence.\n")

