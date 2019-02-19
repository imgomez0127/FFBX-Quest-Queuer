import os
import subprocess
import sys
from ImageScraper import ImageScraper

class ImageGather(object):
	@staticmethod
	def getResolution():
		"""
			This function uses a full screenshot from the ImageScraper to
			get the screen resolution
		"""	
		bbox = ImageScraper(1).getImage().getbbox()  
		return str(bbox[2]) + "x" + str(bbox[3]) 

	def __init__(self,timeFrame,OS="linux"):
		self.__timeFrame = timeFrame
		self.__OS = OS.strip()
		self.__resolution = ImageGather.getResolution()

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

	@resolution.setter
	def resolution(self,resolution):
		self.__resolution = resolution

	def findBoundary(self,boundaryName):
		"""
			Args:	
				boundaryName (str): The name of the boundary box that is being searched for 
			
			This function takes in an input of a bounday box name and outputs the respective
			4-tuple of the bounding box in pixles. This bounding box is contained in 
			box-sizes/box-sizes.cfg
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
		"""
			This function proccesses the commands for which screenshots to take.
			This is done by prompting the user with a menu, for which they respond which pictures they want to take.
			They are also allowed to choose whether or not it should be labeled as a positive or negative example.
			Finally they are prompted whether they want to take more screenshots and if not the program exits.
		"""
		runProgram = True
		PosExampleFlag = True
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
			boxtype = {'a':"autobox",'q':"questbox",'n':"nextbox",'c':"companionbox",'d':"departbox",'r':"requestbox"}
			screenshotType = input(menu).lower()
			while(screenshotType not in choices):
				print("This is not a valid choce \n\n")	
				screenshotType = input(menu).lower()	
			if(screenshotType == "a"):
				self.screenshotbox(PosExampleFlag,boxtype[screenshotType])
			elif(screenshotType == 'q'):
				self.screenshotbox(PosExampleFlag,boxtype[screenshotType])
			elif(screenshotType == 'n'):
				self.screenshotbox(PosExampleFlag,boxtype[screenshotType])
			elif(screenshotType == 'c'):
				self.screenshotbox(PosExampleFlag,boxtype[screenshotType])
			elif(screenshotType == 'd'):
				self.screenshotbox(PosExampleFlag,boxtype[screenshotType])
			elif(screenshotType == 'r'):
				self.screenshotbox(PosExampleFlag,boxtype[screenshotType])
			elif(screenshotType == 's'):
				PosExampleFlag = True if(input("Set flag to [T/F]: ").lower() == "t") else False	
				print(PosExampleFlag)
			else:
				continue
			runProgram = (input("Would you like to gather more screenshots [y/n]: ").lower() == "y")

	def screenshotbox(self,PosExampleFlag,boxtype):
		"""
			Args:
				PosExampleFlag (bool): A flag which represents whether the screenshot is a positive or negative example
				boxtype (str): A string which indicates what type of box is being screenshoted
			
			This function takes a screenshot of the indicated box and saves it in the respective folder location.
			Indicating whether or not it is a Positive or Negative example (as indicated by the user)
			for ease of data labelling
		"""
		box_boundary = self.findBoundary(boxtype)
		fileName = boxtype + ("Pos" if (PosExampleFlag) else "Neg")
		path = boxtype + ("Pos" if (PosExampleFlag) else "Neg") + "Examples"
		imageScraper = ImageScraper(self.__timeFrame,fileName,path,box_boundary)
		imageScraper.takeScreenshots()

if __name__ == "__main__":
	if(len(sys.argv) < 2 or len(sys.argv) > 3):
		print("Usage: python DataGather.py <timeFrame> [Operating System]")
		sys.exit(1)
	if(len(sys.argv) == 2):
		Gatherer = ImageGather(sys.argv[1])
	else:
		Gatherer = ImageGather(int(sys.argv[1]),sys.argv[2])
	Gatherer.gatherData()	

