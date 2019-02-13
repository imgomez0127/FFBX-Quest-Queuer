import os
import re
import subprocess
import sys
import ImageScraper

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
		autobox_boundary = self.findBoundary("autobox")
		return autobox_boundary
if __name__ == "__main__":
	if(len(sys.argv) < 2 or len(sys.argv) > 3):
		print("Usage: python DataGather.py <timeFrame> [Operating System]")
		sys.exit(1)
	if(len(sys.argv) == 2):
		Gatherer = ImageGather(sys.argv[1])
	else:
		Gatherer = ImageGather(sys.argv[1],sys.argv[2])
	print(Gatherer.gatherData())
	
