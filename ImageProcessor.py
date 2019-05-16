"""
    A python class to process all the images within a folder
    it process the images by turning them into a numpy array 
    which can be used for analysis in a machine learning algorithm

    @author Ian Gomez imgomez0127@github
"""
#Python Base Libraries
import json
import os
import os.path
import re
#Installed Libraries
import numpy as np
from PIL import Image
from tensorflow import one_hot,convert_to_tensor
class ImageProcessor(object):
    """
        Args:
            folderPath(str): A string to the folder path that images will 
            be pulled from
    """ 

    @staticmethod
    def toImageTensor(image):
        return convert_to_tensor(np.asarray(image,dtype="float64"))

    def __init__(self,folderPath = "./Screenshots"):
        if(os.path.isdir(folderPath)):
            self.__folderPath = folderPath
        else:
            errMessage = "The input path is not a valid path folder path"
            raise NotADirectoryError(errMessage) 
        self.__processedImages = None
        self.__imageClasses = None

    @property
    def folderPath(self):
        #folder path to process images from
        return self.__folderPath

    @folderPath.setter
    def folderPath(self,newPath):
        self.__folderPath = newPath

    @property
    def processedImages(self):  
        #A list of processed images
        return self.__processdImages

    @processedImages.setter
    def processedImages(self,newImageLst):
        self.__processedImages = newImageLst

    @property
    def imageClasses(self):
        return self.__imageClasses
    
    def __folderImagesToTensor(self,imagePath):
        """
            Args:
                imagePath(str): The path to the image that 
                is to be converted to a numpy array
            Returns:
                imArr(np.array[float64]): Array of matrix representation of images
            This function takes in a path to an image and returns the a 
            numpy array for that image
        """
        im = Image.open(imagePath)
        imArr = convert_to_tensor(np.asarray(im,dtype="float64"))
        im.close()
        return imArr    
    
    def processFolderImages(self):
        """
            This function selects the folderPath memeber variable and 
            turns all images in that file into a numpy array which is storred
            in the member variable processedImages
        """ 
        fileList = os.listdir(self.__folderPath)
        processedImages = []
        for fileName in fileList:
            try:
                fullImagePath = self.__folderPath + "/" + fileName
                imgAsArr = self.__folderImagesToTensor(fullImagePath)
                processedImages.append(imgAsArr) 
            except OSError:
                continue
        self.__processedImages = convert_to_tensor(processedImages,dtype="float64")
        return self.__processedImages

    def classifyImages(self):
        regexPos = re.compile("(Pos)+") 
        imageClasses = []
        fileList = os.listdir(self.__folderPath)
        for fileName in fileList:
            imageClasses.append(1 if (regexPos.findall(fileName) != []) else 0)
        self.__imageClasses = convert_to_tensor(imageClasses,dtype="float64")
        return self.__imageClasses

    def __getHighestCategoryNumber(self,fileLst):
        numberRegex = re.compile("[0-9]+")
        highestCategory = float("-inf")
        for fileName in fileLst:
            matchedLst = numberRegex.findall(fileName)
            if(len(matchedLst) != 2):
                message = "File %s is not formatted in [A-Za-z]+[0-9]+[A-Za-z]+[0-9]+"
                raise ValueError(message%fileName)
            highestCategory = max(int(matchedLst[1]),highestCategory)
        return highestCategory

    def classifyCategoricalImages(self):
        numberRegex = re.compile("[0-9]+")
        fileLst = os.listdir(self.__folderPath)
        highestCategoryNumber = self.__getHighestCategoryNumber(fileLst)
        labels = [int(numberRegex.findall(fileName)[0]) for fileName in fileLst]
        return one_hot(labels,highestCategoryNumber+1)

if __name__ == "__main__":
    imgProc = ImageProcessor("autoboxExamples")
    print(len(os.listdir("autoboxExamples")))
    print(np.shape(imgProc.processFolderImages()[0]))
