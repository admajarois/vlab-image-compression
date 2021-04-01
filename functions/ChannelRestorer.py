import numpy as np

def imageRestorer(redChannelImage, greenChannelImage, blueChannelImage):
    xMax, yMax = np.array(redChanneImage).shape

    restoredImage = []

    for x in range(xMax):
        ySet = []
        for y in range(yMax):
            zSet = [redChannelImage[x][y], greenChannelImage[x][y], blueChannelImage[x][y]]
            ySet.append(zSet)
        restoredImage.append(ySet)
    
    return restoredImage