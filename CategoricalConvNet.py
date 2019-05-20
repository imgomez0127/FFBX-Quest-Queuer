from functools import reduce
import os
import time
import numpy as np
import pandas
from PIL import Image
import pyscreenshot as ImageGrab
from sklearn.model_selection import train_test_split
from tensorflow import keras
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten,Reshape,BatchNormalization
from ImageProcessor import ImageProcessor 
from ConvNet import ConvNet

class CategoricalConvNet(ConvNet):
    def __init__(self, boxname, convLayerAmt, denseLayersAmt,modelDir="models/"):
        super().__init__(boxname,convLayerAmt,denseLayersAmt,modelDir)
        self._imageLabels = self.__classifyImages()


    def __classifyImages(self):
        processor = ImageProcessor(self._filePath)
        image_labels = processor.classifyCategoricalImages()
        if(len(image_labels) == 0):
            raise ValueError("There are no images in that folder")
        return image_labels

    def BuildConvNet(self):
        self.add(Input(shape=self._imageShape))
        for i in range(self._convLayerAmt):
            self.add(Conv2D(self._kernelChannels,self._kernelSize,
                             padding="Valid"))
            self.add(MaxPooling2D(self._poolingSize))
        self.add(Flatten())
        for i in range(self._denseLayersAmt):
            self.add(Dense(100,activation = "relu", use_bias=True))
        self.add(Dense(len(self._imageLabels[0]),activation="softmax"))
        return self.layers

    def train(self):
        trainingImages = self._regularizeImages(self._images)
        trainingLabels = self._imageLabels 
        self.compile(optimizer = keras.optimizers.Adam(lr=.001),
                    loss="categorical_crossentropy",metrics=["accuracy"])
        self.fit(trainingImages,trainingLabels,epochs=100,
                batch_size=trainingLabels.shape[0],validation_split=0.2)
        
if __name__ == "__main__": 
    test_model = CategoricalConvNet("screenbox",5,10)
    print(np.asarray(test_model.imageLabels))
#   test_model.BuildConvNet()
#   test_model.train()
#   predictions = test_model.predict(test_model.images)
#   print(predictions)
#   print(reduce(lambda x,y: x and y,[round(x[0]) for x in predictions] == test_model.imageLabels))
#   print(test_model.imageLabels)
#   test_model.summary()
