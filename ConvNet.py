"""
    A python class to create the convolutional neural network
    which will be used to establish what type of box is being.
    This class inherit from the keras.Sequential model and also has functions which process and regularize the images
@author Ian Gomez imgomez0127@github
"""
from functools import reduce
import os
import time
import numpy as np
import pandas
from PIL import Image
from sklearn.model_selection import train_test_split
from tensorflow import keras,convert_to_tensor
from tensorflow import shape as tfshape
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten,Reshape,BatchNormalization,Input
from sklearn.utils import shuffle
from ImageProcessor import ImageProcessor 
from ImageScraper import ImageScraper

class ConvNet(keras.Sequential):
    def __init__(self, boxname, convLayerAmt, denseLayersAmt,modelDir="models/"):
        super().__init__()
        self._boxname = boxname
        self._convLayerAmt = convLayerAmt 
        self._denseLayersAmt = denseLayersAmt
        self._filePath = "./" + self._boxname + "Examples" 
        self._imageLabels = self._classifyImages()
        self._images = self._processImages() 
        self._imageShape = self._images[0].shape
        self._kernelSize = 3
        self._kernelChannels = 3
        self._poolingSize = 2
        if(not os.path.isdir(modelDir)):
            raise OSError("The input directory " + str(newDir) +" directory does not exist")
        self._modelDir = modelDir

    @property
    def boxname(self):
        #Name of the box which the ConvNet will predict for
        return self._boxname
    
    @property
    def convLayerAmt(self):
        #Amount of Convolution Layers
        return self._convLayerAmt

    @convLayerAmt.setter
    def convLayerAmt(self,convLayerAmt):
        if(type(convLayerAmt) != int):
            raise ValueError("ConvLayerAmt is not of type int")
        self._convLayerAmt = convLayerAmt
    
    @property
    def denseLayersAmt(self):
        #Amount of Dense Layers
        return self._denseLayersAmt
    
    @denseLayersAmt.setter
    def denseLayersAmt(self,denseLayersAmt):
        self._denseLayersAmt = denseLayersAmt
    
    @property
    def imageShape(self):
        return self._imageShape
    
    @imageShape.setter
    def imageShape(self,imageShape):
        self._imageShape = imageShape 

    @property
    def filePath(self):
        #File path for the images
        return self._filePath
    
    @property
    def images(self):
        #A numpy array of images
        return self._images    

    @property
    def kernelSize(self):
        #Size of the convolutional kernel
        return self._kernelSize
    
    @kernelSize.setter
    def kernelSize(self,kernelSize):
        if(type(kernelSize) != int):
            raise ValueError("The input kernelSize is not an int") 
        self._kernelSize == kernelSize
    
    @property
    def kernelChannels(self):
        #The amount of kernels that will be run over the image per convolutional layer
        return self._kernelChannels
    
    @kernelChannels.setter
    def kernelChannels(self,kernelChannels):
        if(type(kernelChannels) != int):
            raise ValueError("The inputted kernelChannels is not of type int")
        self._kernelChannels = kernelChannels

    @property
    def poolingSize(self):
        return self._poolingSize
    
    @poolingSize.setter
    def poolingSize(self,poolingSize):
        if(type(poolingSize) != int):
            raise ValueError("The inputted poolingSize is not of type int")
        self._poolingSize = poolingSize

    @property
    def imageLabels(self):
        return self._imageLabels

    @property
    def modelDir(self):
        #Directory for the model
        return self._modelDir

    @modelDir.setter
    def modelDir(self,newDir):
        if(not os.path.isdir(newDir)):
            raise OSError("The input directory " + str(newDir) +
                            " directory does not exist")
        self._modelDir = newDir

    @property
    def modelPath(self):
        #Path of the model h5 file
        return self.modelDir+self.boxname+".h5" 

    def _processImages(self):
        """
            Returns:
                processedImages(np.array[float64]): Array of images represented as matrices
            This function processes and returns the images in the folder 
            that holds the examples for the box specified by self._boxname
        """
        processor = ImageProcessor(self._filePath)     
        processedImages = processor.processFolderImages()
        if(len(processedImages) == 0):
            raise ValueError("There are no images in that folder")
        return processedImages 

    def _classifyImages(self):
        """
            This function classifies the images in the folder that 
            holds the examples for the box specifed by self._boxname
        """
        processor = ImageProcessor(self._filePath)
        labels = processor.classifyImages()
        if(len(labels) == 0):
            raise ValueError("There are no images in that folder")
        return labels

    def BuildConvNet(self):
        self.add(Input(shape=self._imageShape))
        for i in range(self._convLayerAmt):
            self.add(Conv2D(self._kernelChannels,self._kernelSize,
                             padding="Valid"))
            self.add(MaxPooling2D(self._poolingSize))
        self.add(Flatten())
        for i in range(self._denseLayersAmt):
            self.add(Dense(100,activation = "relu",use_bias=True))
        self.add(Dense(1,activation="sigmoid"))
        return self.layers
            
    def save(self):
        super().save(self.modelPath)

    def grabRegionAsTensor(self,OS): 
        scraper = ImageScraper(self._boxname,OS)
        return ImageProcessor.toImageTensor(scraper.grabScreenRegion())

    def load_weights(self):
        if(not os.path.exists(self.modelPath)):
            raise OSError("The model does not exist") 
        super().load_weights(self.modelPath)
    
    def regularizeImages(self,images):
        return images/255

    def train(self):
        trainingImages = self.regularizeImages(self._images)
        trainingLabels = self._imageLabels
        self.compile(
            optimizer = keras.optimizers.Adam(lr=.001),
            loss="binary_crossentropy",metrics=["accuracy"])
        self.fit(
            trainingImages,
            trainingLabels,
            epochs=100,
            batch_size=trainingLabels.shape[0],
            validation_split=0.2)
        
if __name__ == "__main__": 
    testModel = ConvNet("autobox",3,6)
    testModel.BuildConvNet()
    testModel.train()
    testModel.save()
    predictions = testModel.predict(testModel.images)
    print(predictions)
    print(reduce(lambda x,y: x and y,[round(x[0]) for x in predictions] == np.asarray(testModel.imageLabels)))
    print(testModel.imageLabels)
    testModel.summary()
