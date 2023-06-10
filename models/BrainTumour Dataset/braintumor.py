# -*- coding: utf-8 -*-
"""BrainTumor.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-QlAyF3zJpcZ1p7b58klZG7du_rKtFxE
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

import matplotlib.pyplot as plt
import seaborn as sns
import keras
from keras.models import Sequential
from keras.layers import Dense, Conv2D , MaxPool2D , Flatten , Dropout , BatchNormalization
from keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report,confusion_matrix
from keras.callbacks import ReduceLROnPlateau
import cv2

from google.colab import drive
drive.mount('/content/gdrive')

!unzip gdrive/My\ Drive/brain.zip

import tensorflow as tf



from pathlib import Path



train_dir = Path("brain/Training")
test_dir = Path("brain/Testing")

height=256
width=256

train_files = list(train_dir.glob("*/*"))
test_files = list(test_dir.glob("*/*"))

print(f"Images train set: {len(train_files)}")
print(f"Images test set: {len(test_files)}")

train_dataset = tf.keras.utils.image_dataset_from_directory(
    train_dir,
    
    shuffle=True,
    batch_size=5216,
    image_size=[height, width],
    seed=123
)



train_dataset

class_names = train_dataset.class_names

images, labels = next(iter(train_dataset))

labels[0]

test_dataset = tf.keras.utils.image_dataset_from_directory(
    test_dir,
    
    shuffle=True,
    batch_size=5216,
    image_size=[height, width],
    seed=123
)

test_dataset

class_names = test_dataset.class_names

images1, labels1 = next(iter(test_dataset))

labels = tf.keras.utils.to_categorical(labels, num_classes = 4)



images=images/255
images1=images1/255

labels1 = tf.keras.utils.to_categorical(labels1, num_classes = 4)

labels1[0]

datagen = ImageDataGenerator(
        featurewise_center=False,  # set input mean to 0 over the dataset
        samplewise_center=False,  # set each sample mean to 0
        featurewise_std_normalization=False,  # divide inputs by std of the dataset
        samplewise_std_normalization=False,  # divide each input by its std
        zca_whitening=False,  # apply ZCA whitening
        rotation_range = 30,  # randomly rotate images in the range (degrees, 0 to 180)
        zoom_range = 0.2, # Randomly zoom image 
        width_shift_range=0.1,  # randomly shift images horizontally (fraction of total width)
        height_shift_range=0.1,  # randomly shift images vertically (fraction of total height)
        horizontal_flip = True,  # randomly flip images
        vertical_flip=False)  # randomly flip images


datagen.fit(images)

from keras.models import Sequential
from keras.layers import Flatten,Activation,Dense,Dropout,Conv2D,MaxPool2D

model =Sequential()

#convolution and maxpoollayer
model.add(Conv2D(filters=25,kernel_size=3,
                 strides=2,padding='valid',input_shape=(256,256,3)))
model.add(Activation('relu'))
model.add(MaxPool2D(pool_size=2))

#flatten layer
model.add(Flatten())

#hidden layer
model.add(Dense(16))
model.add(Activation('relu'))

#output layer
model.add(Dense(4))
model.add(Activation('sigmoid'))


model.summary()

model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])



history = model.fit(datagen.flow(images,labels, batch_size = 32) ,epochs = 12 , validation_data = datagen.flow(images1, labels1) )

model.save('braintumor.h5')

from tensorflow.keras.models import load_model
model=load_model('braintumor.h5')







import tensorflow as tf
train_dataset = tf.keras.utils.image_dataset_from_directory(
    img,
    
    shuffle=True,
    batch_size=5216,
    image_size=[256, 256],
    seed=123
)

