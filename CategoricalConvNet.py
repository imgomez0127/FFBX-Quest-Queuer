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

    def __processImages(self):
        processor = ImageProcessor(self.__filePath)
        processedImages = processor.processFolderImages()
        if(len(processedImages) == 0):
            raise ValueError("There are no images in that folder")
        self.__imageLabels = processor.classifyCategoricalImages()
        self.__imageShape = processedImages[0].shape
        return processedImages

    def __computeFlattenSize(self):
        pass

    def BuildConvNet(self):
        self.add(Input(shape=self.__imageShape))
        for i in range(self.__convLayerAmt):
            self.add(Conv2D(self.__kernelChannels,self.__kernelSize,
                             padding="Valid"))
            self.add(MaxPooling2D(self.__poolingSize))
        self.add(Flatten())
        for i in range(self.__denseLayersAmt):
            self.add(Dense(100,activation = "relu", use_bias=True))
        self.add(Dense(len(self.__imageLabels[0]),activation="softmax"))
        return self.layers

    def __regularizeImages(self,images):
        return images/255

    def train(self):
        trainingImages = self.__regularizeImages(self.__images)
        trainingLabels = self.__imageLabels 
        self.compile(optimizer = keras.optimizers.Adam(lr=.001),
                    loss="categorical_crossentropy",metrics=["accuracy"])
        self.fit(trainingImages,trainingLabels,epochs=100,
                batch_size=trainingLabels.shape[0],validation_split=0.2)
        
if __name__ == "__main__": 
    testModel = ConvNet("screenbox",2,5)
    testModel.BuildConvNet()
    testModel.train()
    predictions = testModel.predict(testModel.images)
    print(predictions)
    print(reduce(lambda x,y: x and y,[round(x[0]) for x in predictions] == testModel.imageLabels))
    print(testModel.imageLabels)
    testModel.summary()
