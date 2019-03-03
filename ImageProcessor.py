"""
    A python class to process all the images within a folder
    it process the images by turning them into a numpy array 
    which can be used for analysis in a machine learning algorithm
"""
#Python Base Libraries
import os
import os.path
import re
#Installed Libraries
import numpy as np
from PIL import Image
class ImageProcessor(object):
    """
        Args:
            folderPath(str): A string to the folder path that images will 
            be pulled from
    """ 
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
    
    def __ImageToArray(self,imagePath):
        """
            Args:
                imagePath(str): The path to the image that 
                is to be converted to a numpy array

            This function takes in a path to an image and returns the a 
            numpy array for that image
        """
        im = Image.open(imagePath)
        imArr = np.asarray(im)
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
        imageClasses = []
        for fileName in fileList:
            try:
                fullImagePath = self.__folderPath + "/" + fileName
                imgAsArr = self.__ImageToArray(fullImagePath)
                processedImages.append(imgAsArr) 
                imageClasses.append(self.__classifyImages(fileName))
            except OSError:
                continue
        self.__processedImages = np.asarray(processedImages)
        self.__imageClasses = np.asarray(imageClasses)
        return self.__processedImages

    def __classifyImages(self,fileName):
        regexPos = re.compile("(Pos)+") 
        return 1 if (regexPos.findall(fileName) != []) else 0 

if __name__ == "__main__":
    imgProc = ImageProcessor("autoboxExamples")
    print(len(os.listdir("autoboxExamples")))
    print(np.shape(imgProc.processFolderImages()[0]))
