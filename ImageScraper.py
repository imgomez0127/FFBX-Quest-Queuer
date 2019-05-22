"""
    A Python file for a class to automate the screenshotting process
    which will be used to feed into the Convolutional Neural Network

    Example:
        $python ImageScraper.py <ImageCount> [filePrefix] [path] [boundary 1]
[boundary 2] [boundary 3] [boundary 4]

    @author Ian Gomez imgomez0127@github
"""
#Python Base Libraries
import os
import re
import sys
#Installed Libraries
import pyscreenshot as ImageGrab
class ImageScraper(object):
    """
        Args:
            boxtype(str): String that represents what type of 
            image is being taken
            OS(str): The operating system of the current system
            filePrefix (str): The name of the output file
            path (str): The name of the output path 
    """

    @staticmethod
    def grabScreen():
        return ImageGrab.grab()

    @staticmethod
    def getResolution():
        screenBoundary = ImageScraper.grabScreen().getbbox()
        return str(screenBoundary[2]) + "x" + str(screenBoundary[3])

    def __init__(self,boxtype,OS="linux",filePrefix="Screenshot",path="./Screenshots"):
        self.__boxtype = boxtype
        self.__OS = OS
        self.__filePrefix = filePrefix
        self.__path = path
        self.__resolution = self.getResolution()
        self.__boundary = self.findBoundary(boxtype)
        if(not os.path.exists(self.__path)):
            try:
                os.mkdir(self.__path)
            except:
                raise ValueError("The input path is not a syntactically valid path")
        
    @property
    def filePrefix(self):
        #filePrefix (str): The name of the output file
        return self.__filePrefix

    @filePrefix.setter
    def filePrefix(self,filePrefix):
        self.__filePrefix = str(filePrefix)

    @property
    def path(self):
        #path (str): The name of the output path
        return self.__path
    
    @path.setter
    def path(self,path):
        if(not os.path.exists(self.__path)):
            try:
                os.mkdir(self.__path)
            except:
                raise ValueError("The input path is not a syntactically valid path")
        self.__path = path
    
    @property
    def boundary(self):
    #boundary (:obj:4-tuple of :obj:int): a 4-tuple of integer values that represent the boundary box of the screenshot
        return self.__boundary
    
    @boundary.setter
    def boundary(self,boundary):
        if(len(boundary) != 4):
            raise ValueError("The boundary take in 4 integer inputs")
        for val in boundary:
            if(not isinstance(val,int)):
                raise ValueError("The boundary take in 4 integer inputs")
        self.__boundary = boundary

    @property
    def boxtype(self):
    #boxtype (str): Name of the box to be screenshoted
        return self.__boxtype
    
    @boxtype.setter
    def boxtype(self,boxtype):
        self.__boxtype = boxtype

    @property
    def OS(self):
    #OS (str): Name of the operating system being used by the computer
        return self.__OS
    
    @OS.setter
    def OS(self,OS):
        self.__OS = OS

    @property
    def resolution(self):
        #The screen resolution of the current computer
        return self.__resolution

    def __filterImages(self,fileLst): 
        image_regex = re.compile("jpg|png")
        image_lst = []
        for file_name in fileLst:
            if(image_regex.search(file_name)):
                image_lst.append(file_name)
        return image_lst

    def __getAmountOfImages(self,directory_list):
        image_regex = re.compile("jpg|png") 
        image_amount = 0 
        for image_file in directory_list:
            if(image_regex.findall(image_file) != []):
                image_amount += 1 
        return image_amount

    def __getLatestScreenshot(self,path):
        regex = re.compile("[0-9]+")
        imgLst = self.__filterImages(os.listdir(path))
        if self.__getAmountOfImages(imgLst) == 0:
            return 0
        intLst = [int(regex.findall(im)[0]) for im in imgLst]
        return max(intLst)+1
    

    def __getLatestCategoricalScreenshot(self,path,category):
        regex = re.compile("[0-9]+")
        imgLst = self.__filterImages(os.listdir(path))
        if self.__getAmountOfImages(imgLst) == 0:
            return 0
        try:
            intLst = [int(regex.findall(im)[0]) if(int(regex.findall(im)[1]) == category) else 0 for im in imgLst]
        except (ValueError,KeyError) as e:
            message = "Not all files are not formatted in [A-Za-z]+[0-9]+[A-Za-z]+[0-9]+"
            print(e)
            print(message)
            sys.exit(0)
        return max(intLst)+1 if(max(intLst) != 0) else 0
       
    def findBoundary(self,boundaryName):
        """
            Args:   
                boundaryName (str): The name of the boundary box that 
                is being searched for 

            Returns:
                boundrybox (4-tuple of ints)        
        """
        bboxSetting = "[" + self.__OS.lower() + "-" + boundaryName + "-" + self.__resolution + "]"
        f = open("box-sizes/box-sizes.cfg","r") 
        curLine = f.readline()
        while(curLine != "" and curLine[:-1] != bboxSetting):
            curLine = f.readline()
        bbox = f.readline()
        f.close()
        if(bbox == ""):
            raise ValueError("Could not find boundary in the box-sizes.cfg file")
        return tuple([int(boundary) for boundary in bbox.strip().split(" ")])

    def takeScreenshots(self,screenshotAmount):
        """
            Returns:
                screenshots (list of 2-tuple of (str,Image)): a list of 2-tuples
                where the first item is the screenshot name and the second item
                is the Image object
            
            This function takes screenshots of the given boundary and returns
            a list of screenshots which are tuples of screenshot names and the 
            Image object
        """
        latestScreenshot = self.__getLatestScreenshot(self.path)
        screenshot = [] 
        for i in range(screenshotAmount):
            screenshotNum = str(i+latestScreenshot)
            if(self.__boundary != ()):
                image = ImageGrab.grab(self.boundary)
            else:
                image = ImageGrab.grab()
            filePath = ""
            if(self.__path[0] != "."):
                filePath += "."
            if(self.__path[1] != "/"):
                filePath += "/"
            if(self.__path[-1] == "/"):
                filePath += self.path + self.filePrefix + screenshotNum + ".jpg"
            else:
                filePath += self.path +'/' + self.__filePrefix + \
                            screenshotNum + ".jpg"
            screenshot.append((filePath,image))
        return screenshot

    def takeCategoricalScreenshots(self,screenshotAmount,category):
        """
            Returns:
                screenshots (list of 2-tuple of (str,Image)): a list of 2-tuples
                where the first item is the screenshot name and the second item
                is the Image object
            
            This function takes screenshots of the given boundary and returns
            a list of screenshots which are tuples of screenshot names and the 
            Image object
        """
        latestScreenshot = self.__getLatestCategoricalScreenshot(self.path,category)
        screenshot = [] 
        categoryStr = "Category" + str(category)
        for i in range(screenshotAmount):
            screenshotNum = str(i+latestScreenshot)
            if(self.__boundary != ()):
                image = ImageGrab.grab(self.boundary)
            else:
                image = ImageGrab.grab()
            filePath = ""
            if(self.__path[0] != "."):
                filePath += "."
            if(self.__path[1] != "/"):
                filePath += "/"
            if(self.__path[-1] == "/"):
                filePath += self.path + self.filePrefix + screenshotNum\
                + categoryStr + ".jpg"
            else:
                filePath += self.path + '/' + self.__filePrefix + screenshotNum\
                + categoryStr + ".jpg"
            screenshot.append((filePath,image))
        return screenshot

    def saveScreenshots(self,screenshots):
        """
            Args:
                screenshots (list of 2-tuple of (str,Image)): a list of 2-tuples
                where the first item is the screenshot name and the second item
                is the Image object
            
            This function takes in a list of screenshots and saves them
        """
        for filePath,image in screenshots:
            image.save(filePath)
        
    def grabScreenRegion(self):
        return ImageGrab.grab(self.boundary) 

if __name__ == '__main__':
    print("hello world")
