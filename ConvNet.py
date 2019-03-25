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

class ConvNet(keras.Sequential):
    def __init__(self, boxname, convLayerAmt, denseLayersAmt,modelDir="models/"):
        super().__init__()
        self.__boxname = boxname
        self.__convLayerAmt = convLayerAmt 
        self.__denseLayersAmt = denseLayersAmt
        self.__imageShape = None
        self.__filePath = "./" + self.__boxname + "Examples"
        self.__imageLabels = []
        self.__images = self.__processImages()
        self.__kernelSize = 3
        self.__kernelChannels = 3
        self.__poolingSize = 2
        if(not os.path.isdir(modelDir)):
            raise OSError("The input directory " + str(newDir) +" directory does not exist")
        self.__modelDir = modelDir
    @property
    def boxname(self):
        return self.__boxname
    
    @property
    def convLayerAmt(self):
        return self.__convLayerAmt

    @convLayerAmt.setter
    def convLayerAmt(self,convLayerAmt):
        if(type(convLayerAmt) != int):
            raise ValueError("ConvLayerAmt is not of type int")
        self.__convLayerAmt = convLayerAmt
    
    @property
    def denseLayersAmt(self):
        return self.__denseLayersAmt
    
    @denseLayersAmt.setter
    def denseLayersAmt(self,denseLayersAmt):
        self.__denseLayersAmt = denseLayersAmt
    
    @property
    def imageShape(self):
        return self.__imageShape
    
    @imageShape.setter
    def imageShape(self,imageShape):
        self.__imageShape = imageShape 

    @property
    def filePath(self):
        return self.__filePath
    
    @property
    def images(self):
        return self.__images    

    @property
    def kernelSize(self):
        return self.__kernelSize
    
    @kernelSize.setter
    def kernelSize(self,kernelSize):
        if(type(kernelSize) != int):
            raise ValueError("The input kernelSize is not an int") 
        self.__kernelSize == kernelSize
    
    @property
    def kernelChannels(self):
        return self.__kernelChannels
    
    @kernelChannels.setter
    def kernelChannels(self,kernelChannels):
        if(type(kernelChannels) != int):
            raise ValueError("The inputted kernelChannels is not of type int")
        self.__kernelChannels = kernelChannels
    @property
    def poolingSize(self):
        return self.__poolingSize
    
    @poolingSize.setter
    def poolingSize(self,poolingSize):
        if(type(poolingSize) != int):
            raise ValueError("The inputted poolingSize is not of type int")
        self.__poolingSize = poolingSize

    @property
    def imageLabels(self):
        return self.__imageLabels

    @property
    def modelDir(self):
        return self.__modelDir

    @modelDir.setter
    def modelDir(self,newDir):
        if(not os.path.isdir(newDir)):
            raise OSError("The input directory " + str(newDir) +" directory does not exist")
        self.__modelDir = newDir
    @property
    def modelPath(self):
        return self.modelDir+self.boxname+".h5" 
    def __processImages(self):
        processor = ImageProcessor(self.__filePath)     
        processedImages = processor.processFolderImages()
        if(len(processedImages) == 0):
            raise ValueError("There are no images in that folder")
        self.__imageLabels = processor.classifyImages()
        self.__imageShape = processedImages[0].shape
        return processedImages 
    def __computeFlattenSize(self):
        pass
    def BuildConvNet(self,output = 1):
        self.add(Reshape((60,150,3)))
        for i in range(self.__convLayerAmt):
            self.add(Conv2D(self.__kernelChannels,self.__kernelSize,
                             padding="Valid"))
            self.add(MaxPooling2D(self.__poolingSize))
        self.add(Flatten())
        for i in range(self.__denseLayersAmt):
            self.add(Dense(100,activation = "relu", use_bias=True))
        self.add(Dense(output,activation="sigmoid"))
        return self.layers

    def save(self):
        super().save(self.modelPath)
    
    def load_weights(self):
        if(not os.exists(self.modelPath)):
            raise OSError("The model does not exist") 
        super.load_weights(self.modelPath)
    
    def __regularizeImages(self,images):
        return images/255
    def train(self):
        trainingImages = self.__regularizeImages(self.__images)
        trainingLabels = self.__imageLabels 
        self.compile(optimizer = keras.optimizers.Adam(lr=.001),
                    loss="binary_crossentropy",metrics=["accuracy"])
        self.fit(trainingImages,trainingLabels,epochs=100,
                batch_size=trainingLabels.shape[0],validation_split=0.2)
        
if __name__ == "__main__": 
    testModel = ConvNet("autobox",2,5)
    testModel.BuildConvNet()
    testModel.train()
    predictions = testModel.predict(testModel.images)
    print(predictions)
    print(reduce(lambda x,y: x and y,[round(x[0]) for x in predictions] == testModel.imageLabels))
    print(testModel.imageLabels)
    testModel.summary()
