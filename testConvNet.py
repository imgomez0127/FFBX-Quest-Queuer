from tensorflow import keras
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten,Activation,LeakyReLU,Dropout,Reshape,BatchNormalization
import numpy as np
from tensorflow.keras.datasets import mnist
from ImageProcessor import ImageProcessor
from math import ceil
(x_train,y_train),(x_test,y_test) = mnist.load_data()
print(x_train.shape)
processor = ImageProcessor("./autoboxExamples")
images = processor.processFolderImages()
labels = processor.classifyImagesAsPositiveOrNegative()
model = keras.Sequential()
model.add(Reshape((60,150,3)))
model.add(BatchNormalization(axis=-2))
model.add(BatchNormalization())
model.add(Conv2D(6,(3,3),activation="relu",padding="same"))
model.add(MaxPooling2D(3))
model.add(Conv2D(32,(3,3),activation="relu",padding="same"))
model.add(MaxPooling2D(3))
model.add(BatchNormalization())
model.add(Flatten())
model.add(BatchNormalization())
model.add(Dense(1000,activation="relu"))
model.add(Dense(1000,activation="relu"))
model.add(Dense(1,activation="sigmoid"))
model.compile(optimizer = keras.optimizers.SGD(lr=.01),loss="binary_crossentropy",metrics=["accuracy"])
model.fit(images,labels,epochs=100,batch_size=10)
predictions = model.predict(images,batch_size=images.shape[0])
print(predictions)
print(list(labels))
print([round(x[0]) for x in predictions] == labels)
model.summary()
