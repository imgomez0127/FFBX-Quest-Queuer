"""
	A Python file for a class to automate the screenshotting process
	which will be used to feed into the Convolutional Neural Network

	Example:
		$python ImageScraper.py <ImageCount> [fileName] [path] [boundary 1] [boundary 2] [boundary 3] [boundary 4]
"""
import PIL
import os
import sys
from PIL import ImageGrab
import time
class ImageScraper(object):
	"""
		Args:
			imageCount (int): The amount of images that should be taken
			fileName (str): The name of the output file
			path (str): The name of the output path 
			boundaries (:obj:4-tuple of :obj:int): a 4-tuple of integer values that represent the boundary box of the screenshot
	"""
	def __init__(self,imageCount,fileName="screenshot",path="./images",boundaries=()):
		self.__imageCount = imageCount
		self.__fileName = fileName
		self.__boundaries = boundaries
		self.__path = path
		if(not os.path.exists(self.__path)):
			try:
				os.mkdir(self.__path)
			except:
				raise ValueError("The input path is not a syntactically valid path")
		
	@property
	def imageCount(self):
		# imageCount (int): the amount of images that should be taken 
		return self.__imageCount

	@imageCount.setter
	def imageCount(self,imageCount):
		if(not isinstance(isinstance(imageCount,int))):
			try:
				self.__imageCount = int(imageCount)
			except:
				raise ValueError("The input for the amount of images is not convertable to an integer.")
		if(imageCount > 1000):
			raise ValueError("Image Count is too high please chose a smaller amount of images to scrape.")
		self.__imageCount = imageCount

	@property
	def fileName(self):
		#fileName (str): The name of the output file
		return self.__fileName

	@fileName.setter
	def fileName(self,fileName):
		self.__fileName = str(fileName)

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
	#boundaries (:obj:4-tuple of :obj:int): a 4-tuple of integer values that represent the boundary box of the screenshot
		return self.__boundary
	
	@boundary.setter
	def boundary(self,boundary):
		if(len(boundary) != 4):
			raise ValueError("The boundaries take in 4 integer inputs")
		for val in boundary:
			if(not isinstance(int,val)):
				raise ValueError("The boundaries take in 4 integer inputs")
		self.__boundary = boundary

	def takeScreenshots(self):
		"""
			This function takes an screenshot for the range 0-imageCount
			screenshots the given boundary every 1 second and saves it with the given fileName 
			in a jpg format and outputs it to the  given filePath
		"""
		for i in range(self.__imageCount):
			screenshot = ImageGrab.grab(self.__boundaries)
			if(self.__path[-1] == "/"):
				filePath = self.__path+self.__fileName+str(i+1)+".jpg"
			else:
				filePath = self.__path+'/' + self.__fileName + str(i) + ".jpg"
			screenshot.save(filePath)
			time.sleep(1)

if __name__ == '__main__':
	if(len(sys.argv)<1 or len(sys.argv) > 7):
		print("Usage: python ImageScraper.py <ImageCount> [fileName] [path] [boundary 1] [boundary 2] [boundary 3] [boundary 4]")
		sys.exit(1)

	Scraper = ImageScraper(5)
	Scraper.takeScreenshots()