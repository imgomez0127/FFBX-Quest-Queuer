import os
import time
import numpy as np
import pandas
from PIL import Image
import pyscreenshot as ImageGrab
from sklearn.model_selection import train_test_split
from tensorflow import keras
import ImageProcessor 

class ConvNet(keras.Sequential):
	def __init__(self, boxname, convAmt, hiddenLayers):
		super().__init__()
		self.__boxname = boxname
		self.__convAmt = convAmt
		self.__hiddenLayers = hiddenLayers
		self.__imageSize = 0

	@property
	def boxname(self):
		return self.__boxname
	
	@property
	def convAmt(self):
		return self.__convAmt

	@convAmt.setter
	def convAmt(self,convAmt):
		self.__convAmt = convAmt
	
	@property
	def hiddenLayers(self):
		return self.__hiddenLayers
	
	@hiddenLayers.setter
	def hiddenLayers(self,hiddenLayers):
		self.__hiddenLayers = hiddenLayers
	
	
