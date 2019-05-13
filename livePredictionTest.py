from time import sleep
from tensorflow import reshape
from ConvNet import ConvNet

if __name__ == "__main__":
    autoboxNet = ConvNet("autobox",2,5)
    autoboxNet.BuildConvNet()
    autoboxNet.load_weights()
    while(True):
        curImg = reshape(autoboxNet.grabRegionAsTensor("windows")/255,[1,60,150,3])
        print(int(autoboxNet.predict(curImg)))
        sleep(1)
