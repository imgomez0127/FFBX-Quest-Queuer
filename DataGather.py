import os
import re
import subprocess
import sys
import time
from ImageScraper import ImageScraper

class ImageGather(object):
	def __init__(self,timeFrame,OS="linux"):
		self.__timeFrame = timeFrame
		self.__OS = OS.strip()

	@property
	def timeFrame(self):
		return self.__timeFrame

	@timeFrame.setter
	def timeFrame(self,timeFrame):
		self.__timeFrame = timeFrame

	def findBoundary(self,boundaryName):
		bboxSetting = "[" + self.__OS.lower() + "-" + boundaryName + "]"
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
		runProgram = True
		while(runProgram):
			menu = """A - Fetch Auto Box Pictures
Q - Fetch Quest Box Pictures
N - Fetch Next Box Pictures
Please Input a choice : """
			choices = ['a','q','n']
			screenshotType = input(menu).lower()
			while(screenshotType not in choices):
				print("This is not a valid choce \n\n")	
				screenshotType = input(menu).lower()	
			if(screenshotType == "a"):
				self.screenshotAutobox()
			elif(screenshotType == 'q'):
				self.screenshotQuestbox()
			else:
				self.screenshotNextbox()
			runProgram = (input("Would you like to gather more screenshots [y/n]: ").lower() == "y")
				
	def screenshotQuestbox(self):
		questbox_boundary = self.findBoundary("questbox")
		imageScraper = ImageScraper(self.__timeFrame,"questboxPos","questboxPosExamples",questbox_boundary)
		imageScraper.takeScreenshots()
	def screenshotAutobox(self):
		autobox_boundary = self.findBoundary("autobox")
		imageScraper = ImageScraper(self.__timeFrame,"autoboxPos","autoboxPosExamples",autobox_boundary)
		imageScraper.takeScreenshots()	
	def screenshotNextbox(self):
		nextbox_boundar = self.findBoundary("nextbox")
		imageScraper = ImageScraper(self.__timeFrame,"autoboxPos","autoboxPosExamples",autobox_boundary)
if __name__ == "__main__":
	if(len(sys.argv) < 2 or len(sys.argv) > 3):
		print("Usage: python DataGather.py <timeFrame> [Operating System]")
		sys.exit(1)
	if(len(sys.argv) == 2):
		Gatherer = ImageGather(sys.argv[1])
	else:
		Gatherer = ImageGather(int(sys.argv[1]),sys.argv[2])
	Gatherer.gatherData()	
