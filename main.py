import json
from time import sleep
import os.path
from pymouse import PyMouse
from tensorflow import reshape
from ConvNet import ConvNet
from CategoricalConvNet import CategoricalConvNet
from numpy import argmax
def findBoundary(boundaryName,OS,resolution):
    """
        Args:   
            boundaryName (str): The name of the boundary box that 
            is being searched for 

        Returns:
            boundrybox (4-tuple of ints)        
    """
    bboxSetting = "[" + OS.lower() + "-" + boundaryName + "-" + resolution + "]"
    f = open("box-sizes/box-sizes.cfg","r") 
    curLine = f.readline()
    while(curLine != "" and curLine[:-1] != bboxSetting):
        curLine = f.readline()
    bbox = f.readline()
    f.close()
    if(bbox == ""):
        raise ValueError("Could not find boundary in the box-sizes.cfg file")
    return [int(boundary) for boundary in bbox.strip().split(" ")]
if __name__ == "__main__":
    screenNet = CategoricalConvNet("screenbox",3,5)
    screenNet.BuildConvNet()
    screenNet.load_weights()
    autoboxNet = ConvNet("autobox",3,6)
    autoboxNet.BuildConvNet()
    autoboxNet.load_weights()
    mouse = PyMouse()
    autobox_boundary = findBoundary("autobox","windows","1920x1080")
    nextbox_boundary = findBoundary("nextbox","windows","1920x1080") 
    departbox_boundary = findBoundary("requestbox","windows","1920x1080") 
    if(not os.path.exists("./screenboxExamples/screenMap.json")):
        raise OSError("./screenboxExamples/screenMap.json does not exist")
    with open("./screenboxExamples/screenMap.json","r") as f:
        screenMap = json.load(f)
    while(True):  
        cur_screen = reshape(screenNet.grabRegionAsTensor("windows")/255,[1]+list(screenNet.imageShape))
        print("Screen Prediction: %s" % screenMap[str(argmax(screenNet.predict(cur_screen)))])
        cur_autobox = reshape(autoboxNet.grabRegionAsTensor("windows")/255,[1]+list(autoboxNet.imageShape))
        print("Autobox Prediction %s" % screenMap[str(int(autoboxNet.predict(cur_autobox)))])
        if(argmax(screenNet.predict(cur_screen))==0):
            if(int(autoboxNet.predict(cur_autobox)) == 0):
                mouse.click(autobox_boundary[0]+10,autobox_boundary[1]+10)
        elif(argmax(screenNet.predict(cur_screen))==1):
            mouse.click(nextbox_boundary[0]+10,nextbox_boundary[1]+10)
        elif(argmax(screenNet.predict(cur_screen))==2):
            mouse.click(departbox_boundary[0]+10,departbox_boundary[1]+10)
        sleep(1)
