"""
    A python script to automate the image gathering process for building the Convolutional
    Neural Network. 
    Example:
        $pyhton ImageGather.py <timeFrame> [Operating System]
"""
#Python Base Libraries
import os
import subprocess
import sys
#Self Made Libraries
from ImageScraper import ImageScraper

class ImageGather(object):
    """
        Args:
            timeFrame(int): The time frame for which the Images should be screenshotted
            usually taking one picture per second           

            OS(str): The current operating system the user is using
    """
    @staticmethod
    def determineResolution():
        bbox = ImageScraper.grabScreen().getbbox()  
        return str(bbox[2]) + "x" + str(bbox[3]) 

    def __init__(self,timeFrame,OS="linux"):
        self.__timeFrame = timeFrame
        self.__OS = OS.strip()
        self.__resolution = ImageGather.determineResolution()

    @property
    def timeFrame(self):
        #The amount of time to take pictures over
        return self.__timeFrame

    @timeFrame.setter
    def timeFrame(self,timeFrame):
        self.__timeFrame = timeFrame
    
    @property
    def OS(self):
        #The Operating System of the current computer
        return self.__OS

    @OS.setter
    def OS(self,OS):
        self.__OS = OS
    
    @property
    def resolution(self):
        #The screen resolution of the current computer
        return self.__resolution

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
    
    def gatherData(self):
        #This function proccesses the commands for which screenshots to take.
        runProgram = True
        PosExample = True
        while(runProgram):
            menu = """A - Fetch Auto Box Pictures
Q - Fetch Quest Box Pictures
N - Fetch Next Box Pictures
C - Fetch Companion Box Pictures
D - Fetch Depart Box Pictures
R - Fetch Request Box Pictures
S - Set Positive Example Flag
Please Input a choice : """
            choices = ['a','q','n','c','d','r','s']
            boxtype = {'a':"autobox",
                       'q':"questbox",
                       'n':"nextbox",
                       'c':"companionbox",
                       'd':"departbox",
                       'r':"requestbox"}
            screenshotType = input(menu).lower()
            while(screenshotType not in choices):
                print("This is not a valid choce \n\n") 
                screenshotType = input(menu).lower()    
            if(screenshotType == 's'):
                PosExample = True if(input("Set flag to [T/F]: ").lower() == "t") \
                else False  
            elif(screenshotType in choices):
                self.gatherScreenshots(PosExample,boxtype[screenshotType])
            else:
                continue
            runProgram = input("Would you like to gather more screenshots [y/n]: ").lower() == "y"
    
    def gatherScreenshots(self,PosExample,boxtype):
        """
            Args:
                PosExample (bool): positive or negative example
                boxtype (str): A string which indicates 
                               what type of box is being screenshoted
            
            This function takes a screenshot of the indicated box 
            and saves it in the respective folder location. Indicating whether 
            or not it is a Positive or Negative example 
            (as indicated by the user) for ease of data labelling
        """
        boundary = self.findBoundary(boxtype)
        fileName = boxtype + ("Pos" if (PosExample) else "Neg")
        path = boxtype + "Examples"
        imageScraper = ImageScraper(self.__timeFrame,fileName,path,boundary)
        imageScraper.takeScreenshots()

    def gatherCategoricalScreenshots(self,categoryNum,boxtype):
        boundary = self.findBoundary(boxtype)
        fileName = boxType + str(categoryNum) + "Class"
        path = boxtype + "Examples"
        imageScraper = ImageScraper(self.__timeFrame,fileName,path,boundary)
        imageScraper.takeScreenshots()

if __name__ == "__main__":
    if(len(sys.argv) < 2 or len(sys.argv) > 3):
        print("Usage: python ImageGather.py <timeFrame> [Operating System]")
        sys.exit(1)
    if(len(sys.argv) == 2):
        Gatherer = ImageGather(sys.argv[1])
    else:
        Gatherer = ImageGather(int(sys.argv[1]),sys.argv[2])
    Gatherer.gatherData()   

