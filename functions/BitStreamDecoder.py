import cv2
import numpy as np

def decoder(bitStream, redStreamDecoder, greenStreamDecoder, blueStreamDecoder):
    codeStream = bitStreamDecode()
    if codeStream == []:
        while codeSearch(bitStream, redStreamDecoder, 5) != 'seperator':
            code = codeSearch(bitStream, redStreamDecoder, 5)
            codeStream.append(redStreamDecoder[code])
            bitStream = bitStream.replace(code, '',1)
        
        code = codeSearch(bitStream, redStreamDecoder, 5)
        bitStream = bitStream.replace(code, '', 1)
        print('Red over, Green started')

        while codeSearch(bitStream, greenStreamDecoder, 5) != 'seperator':
            code = codeSearch(bitStream, greenStreamDecoder, 5)
            codeStream.append(greenStreamDecoder[code])
            bitStream = bitStream.replace(code, '', 1)
        
        code = codeSearch(bitStream, greenStreamDecoder, 5)
        bitStream = bitStream.replace(code, '', 1)
        print('Green over, Blue Started')

        while bitStream != '':
            code = codeSearch(bitStream, blueStreamDecoder, 5)
            codeStream.append(blueStreamDecoder[code])
            bitStream = bitStream.replace(code, '', 1)

    return codeStream

def codeSearch(smallBitStream, searchDict, slicingIndex):
    code = smallBitStream[:slicingIndex]
    if searchDict.get(code, None) == None:
        return codeSearch(smallBitStream, searchDict, slicingIndex + 1)
    else:
        return code
    
def bitStreamDecode():
    fileToBeDecoded = cv2.imread('mona88.jpg')
    fileToBeDecoded = cv2.cvtColor(fileToBeDecoded, cv2.COLOR_BGR2RGB)

    fileX, fileY, fileZ = fileToBeDecoded.shape
    fileSize = fileX*fileY*fileZ

    decodeStream = []
    for z in range(fileZ):
        for x in range(fileX):
            for y in range(fileZ):
                decodeStream.append(fileToBeDecoded[x][y][z])
                
    return decodeStream