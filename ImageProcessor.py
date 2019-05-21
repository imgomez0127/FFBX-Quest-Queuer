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
    def __filterImages(self,fileLst): 
        image_regex = re.compile("jpg|png")
        image_lst = []
        for file_name in fileLst:
            if(image_regex.search(file_name)):
                image_lst.append(file_name)
        return image_lst
 
    def processFolderImages(self):
        """
            This function selects the folderPath memeber variable and 
            turns all images in that file into a numpy array which is storred
            in the member variable processedImages
        """ 
        imageLst = self.__filterImages(os.listdir(self.__folderPath))
        processedImages = []
        for imageName in imageLst:
            try:
                fullImagePath = self.__folderPath + "/" + imageName
                imgAsArr = self.__folderImagesToTensor(fullImagePath)
                processedImages.append(imgAsArr) 
            except OSError:
                continue
        self.__processedImages = convert_to_tensor(processedImages,dtype="float64")
        return self.__processedImages

    def classifyImages(self):
        regexPos = re.compile("(Pos)+") 
        imageClasses = []
        imageLst = self.__filterImages(os.listdir(self.__folderPath))
        for imageName in imageLst:
            imageClasses.append(1 if (regexPos.findall(imageName) != []) else 0)
        self.__imageClasses = convert_to_tensor(imageClasses,dtype="float64")
        return self.__imageClasses

    def __getHighestCategoryNumber(self,imageLst):
        print(imageLst)
        numberRegex = re.compile("[0-9]+")
        highestCategory = float("-inf")
        for imageName in imageLst:
            matchedLst = numberRegex.findall(imageName)
            if(len(matchedLst) != 2):
                message = "File %s is not formatted in [A-Za-z]+[0-9]+[A-Za-z]+[0-9]+"
                raise ValueError(message%imageName)
            highestCategory = max(int(matchedLst[1]),highestCategory)
        return highestCategory

    def classifyCategoricalImages(self):
        numberRegex = re.compile("[0-9]+")
        imageLst = self.__filterImages(os.listdir(self.__folderPath))
        highestCategoryNumber = self.__getHighestCategoryNumber(imageLst)
        labels = [int(numberRegex.findall(imageName)[1]) for imageName in imageLst]
        return one_hot(labels,highestCategoryNumber+1)

if __name__ == "__main__":
    imgProc = ImageProcessor("autoboxExamples")
    print(len(os.listdir("autoboxExamples")))
    print(np.shape(imgProc.processFolderImages()[0]))
