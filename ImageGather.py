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

    def __init__(self,timeFrame,OS="linux"):
        self.__timeFrame = timeFrame
        self.__OS = OS.strip()

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
X - Fetch Screen Box Pictures
S - Set Positive Example Flag
Please Input a choice : """
            choices = {'a','q','n','c','d','r','x','s'}
            boxtype = {'a':"autobox",
                       'q':"questbox",
                       'n':"nextbox",
                       'c':"companionbox",
                       'd':"departbox",
                       'r':"requestbox",
                       'x':"screenbox"}
            screenshotType = input(menu).lower()
            while(screenshotType not in choices):
                print("This is not a valid choce \n\n") 
                screenshotType = input(menu).lower()    
            if(screenshotType == 's'):
                PosExample = True if(input("Set flag to [T/F]: ").lower() == "t") \
                else False  
            elif(screenshotType == "x"):
                self.gatherCategoricalScreenshots(boxtype[screenshotType])
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
        fileName = boxtype + ("Pos" if (PosExample) else "Neg")
        path = boxtype + "Examples"
        imageScraper = ImageScraper(boxtype,self.__OS,fileName,path)
        screenshots = imageScraper.takeScreenshots(self.__timeFrame)
        imageScraper.saveScreenshots(screenshots) 

    def gatherCategoricalScreenshots(self,boxtype):
        try:
            category_num = int(input("Input the category number: "))
        except ValueError:
            print("You did not input a number")
            return
        filePrefix = boxtype
        path = boxtype + "Examples"
        imageScraper = ImageScraper(boxtype,self.__OS,filePrefix,path)
        screenshots = imageScraper.takeCategoricalScreenshots(
                        self.__timeFrame,
                        category_num)
        imageScraper.saveScreenshots(screenshots)


if __name__ == "__main__":
    if(len(sys.argv) < 2 or len(sys.argv) > 3):
        print("Usage: python ImageGather.py <timeFrame> [Operating System]")
        sys.exit(1)
    if(len(sys.argv) == 2):
        Gatherer = ImageGather(sys.argv[1])
    else:
        Gatherer = ImageGather(int(sys.argv[1]),sys.argv[2])
    Gatherer.gatherData()   

