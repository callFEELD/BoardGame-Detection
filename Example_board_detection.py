"""
Example Board Detection
@file           Example_board_detection.py
@description    Contains an example to extract the game board from
                an given image.
@author         callFEELD
@version        0.1
"""

# Imports
from src.board_detection import board_detection as bd
import cv2
import numpy as np
import imutils

fname = "data/20191113_134305.jpg"
#fname = "data/20191113_134320.jpg" # top down view
#fname = "data/20191113_134334.jpg"
#fname = "data/20191113_134324.jpg"
fname = "data/20191113_134307.jpg"


# image loading and preperation
image = cv2.imread(fname)
image = cv2.resize(image,(int(4032/4), int(2268/4)))
oimage = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# finding chessboard
corners = bd.find_chessboard(gray, (7,7))
if corners is not None:
    cv2.drawChessboardCorners(image, (7,7), corners, 1)
    chessboard_corners = bd.estimate_chessboard8x8_corners(corners, display_points=True, image=image)
    wrapped = bd.get_chessboard(oimage, chessboard_corners)

# Show results
cv2.imshow('Corners and Lines',image)
cv2.imshow('Chessboard',wrapped)

# De-allocate any associated memory usage   
if cv2.waitKey(0) & 0xff == 27:  
    cv2.destroyAllWindows()  