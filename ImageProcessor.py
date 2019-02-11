import os
import os.path
import numpy as np
from PIL import Image
class ImageProcessor(object):
	def __init__(self,folderPath = "./Screenshots"):
		if(os.path.isdir("./Screenshots")):
			self.__folderPath = folderPath
		else:
			raise NotADirectoryError("The input path to the screenshots is not a valid path to a folder") 
		self.__processedImages = []
	@property
	def folderPath(self):
		return self.__folderPath
	@folderPath.setter
	def folderPath(self,newPath):
		self.__folderPath = newPath
	@property
	def processedImages(self):	
		return self.__processdImages
	@processedImages.setter
	def processedImages(self,newImageLst):
		self.__processedImages = newImageLst
	def ImageToArray(self,imagePath):
		im = Image.open(imagePath)
		imArr = np.asarray(im)
		im.close()
		return imArr	
	def processFolderImages(self):
		fileList = os.listdir(self.__folderPath)
		for fileName in fileList:
			try:
				self.__processedImages.append(self.ImageToArray(self.__folderPath + "/" + fileName)) 
			except OSError:
				continue
		return self.__processedImages
if __name__ == "__main__":
	imgProc = ImageProcessor()
	print(imgProc.processFolderImages())
