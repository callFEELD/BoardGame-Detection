"""
Example Mouse Callback
@file           Example_Mouse_Callback.py
@description    This file contains an example of how to find the
                4 corner points of the chessboard manually
@author         callFEELD
@version        0.1
"""

# Imports
from src import board_detection as bd
import cv2


RESIZE_FACTOR = 6

file_name = "data/20200228_181947.jpg"

# read the image and make it smaller
image = cv2.imread(file_name)
image = cv2.resize(image, (int(4032/RESIZE_FACTOR), int(2268/RESIZE_FACTOR)))
cimage = image.copy()

fourpoints = []

# mouse callback function
def mouse_callback(event,x,y,flags,param):
    global fourpoints
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(fourpoints) < 4:
            fourpoints.append([x, y])
        else:
            fourpoints = []
            fourpoints.append([x, y])
        print(x, y)
        print(fourpoints)

        if len(fourpoints) == 4:
            wrapped = bd.get_chessboard_perspective(cimage, fourpoints)
            cv2.imshow('Chessboard', wrapped)


# Show results
cv2.imshow('image', image)
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.setMouseCallback('image', mouse_callback)


# De-allocate any associated memory usage
if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()
