from tensorflow import keras
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten
import numpy as np
from ImageProcessor import ImageProcessor
processor = ImageProcessor("./autoboxExamples")
images = np.asarray(processor.processFolderImages())
labels = np.asarray(processor.imageClasses)
model = keras.Sequential()
model.add(Conv2D(3,3,padding="same",activation="relu"))
model.add(Flatten())
model.add(Dense(1,activation="softmax"))
model.compile(optimizer = keras.optimizers.Adam(lr=.0001),loss="categorical_crossentropy",metrics=["accuracy"])
model.fit(images,labels,epochs=100,batch_size=1)
