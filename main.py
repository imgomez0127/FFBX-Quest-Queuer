from time import sleep
from tensorflow import reshape
from ConvNet import ConvNet
from CategoricalConvNet import CategoricalConvNet
from numpy import argmax
if __name__ == "__main__":
    screenNet = CategoricalConvNet("screenbox",5,10)
    screenNet.BuildConvNet()
    screenNet.load_weights()
    autoboxNet = ConvNet("autobox",3,6)
    autoboxNet.BuildConvNet()
    autoboxNet.load_weights()

    while(True):  
        cur_screen = reshape(screenNet.grabRegionAsTensor("windows")/255,[1]+list(screenNet.imageShape))
        
        if(int(screenNet.predict(curImg)) == 0):
            cur_autobox = reshape(autoboxNet.grabRegionAsTensor("windows")/255,[1]+list(autoboxNet.imageShape))
            print(int(autoboxNet.predict(curImg)))
        sleep(1)
