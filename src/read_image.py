import cv2

def readImage(path):
    imgData = cv2.imread(path)
    if imgData is None:
        print("INVALID IMAGE PATH : " + path)
    return imgData