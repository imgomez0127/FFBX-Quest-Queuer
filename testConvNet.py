from tensorflow import keras
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten,Activation,LeakyReLU,Dropout,Reshape,BatchNormalization,Input
import numpy as np
from tensorflow.keras.datasets import mnist
from ImageProcessor import ImageProcessor
from math import ceil
(x_train,y_train),(x_test,y_test) = mnist.load_data()
print(x_train.shape)
processor = ImageProcessor("./autoboxExamples")
images = processor.processFolderImages()
images /= 255
print(images[0].shape)
labels = processor.classifyImages()
model = keras.Sequential()
Input(shape=(None,3,60,150))
model.add(Conv2D(32,(5,5),activation="relu",padding="valid"))
model.add(MaxPooling2D(2))
model.add(Conv2D(32,(5,5),activation="relu",padding="valid"))
model.add(MaxPooling2D(2))
model.add(Flatten())
model.add(Dense(200,activation="relu"))
model.add(Dense(100,activation="relu"))
model.add(Dense(1,activation="sigmoid"))
model.compile(optimizer = keras.optimizers.SGD(lr=.01),loss="binary_crossentropy",metrics=["accuracy"])
model.fit(images,labels,epochs=10,batch_size=1)
predictions = model.predict(images,batch_size=images.shape[0])
print(predictions)
print(list(labels))
print(round(predictions[0][0]))
print([round(x[0]) for x in predictions] == [int(x) for x in labels])
model.summary()
