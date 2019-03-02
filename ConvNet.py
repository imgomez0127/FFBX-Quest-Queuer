import os
import time
import numpy as np
import pandas
from PIL import Image
import pyscreenshot as ImageGrab
from sklearn.model_selection import train_test_split
from tensorflow import keras
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten
from ImageProcessor import ImageProcessor 

class ConvNet(keras.Sequential):
    @staticmethod
    def __init__(self, boxname, convLayerAmt, denseLayers):
        super().__init__()
        self.__boxname = boxname
        self.__convLayerAmt = convLayerAmt
        self.__denseLayers = denseLayers
        self.__imageShape = 0
        self.__filePath = "./" + self.__boxname + "Examples"
        self.__images = self.__processImages()
        self.__kernelSize = 3
        self.__kernelChannels = 3
        self.__poolingSize = 2
    @property
    def boxname(self):
        return self.__boxname
    
    @property
    def convLayerAmt(self):
        return self.__convLayerAmt

    @convLayerAmt.setter
    def convLayerAmt(self,convLayerAmt):
        self.__convLayerAmt = convLayerAmt
    
    @property
    def denseLayers(self):
        return self.__denseLayers
    
    @denseLayers.setter
    def denseLayers(self,denseLayers):
        self.__denseLayers = denseLayers
    
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

    def __processImages(self):
        processor = ImageProcessor(self.__filePath)     
        processedImages = processor.processFolderImages()
        if(len(processedImages) === 0):
            raise ValueError("There are no images in that folder")
        self.__imageShape = processedImages[0].shape
        return processedImages 
    def __computeFlattenSize(self):
        
    def BuildConvNet(self):
        for _ in range(self.__convLayerAmt):
            self.add(Conv2D(self.__channels,self.__kernelSize,
                            padding="same",activation="relu"))
            self.add(MaxPooling2D(self.__poolingSize))
        self.add(Flatten())
        for i in range(self.__denseLayers):
            self.add(Dense(
        self.add(Dense(1,activation"softmax"))
        return self.layers

if __name__ == "__main__":
    yeet = ConvNet("autobox",2,5)
    print(yeet.BuildConvNet())
