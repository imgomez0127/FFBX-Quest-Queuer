from time import sleep
from ConvNet import ConvNet

if __name__ == "__main__":
    autoboxNet = ConvNet("autobox",2,5)
    autoboxNet.BuildConvNet()
    autoboxNet.load_weights()
    while(True):
        curImg = autoboxNet.grabRegionAsTensor("windows")/255
        print(int(autoboxNet.predict(curImg)))
        sleep(1)
