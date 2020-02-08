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
from src import ColorDetector
import cv2
import numpy as np
import imutils

fname = "data/20191113_134305.jpg"
#fname = "data/20191113_134320.jpg" # top down view
fname = "data/20191113_134334.jpg"
#fname = "data/20191113_134324.jpg"
#fname = "data/20191113_134307.jpg"


# BOARD COLORS
HSV_WHITE_SQUARE_LOWER = np.array([0, 11, 193])
HSV_WHITE_SQUARE_UPPER = np.array([40, 80, 261])

HSV_BLACK_SQUARE_LOWER = np.array([-10, 0, 48])
HSV_BLACK_SQUARE_UPPER = np.array([121, 79, 218])


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

    cv2.imwrite("result.png", wrapped)

    white_color_mask = ColorDetector.get_color_mask(wrapped, HSV_WHITE_SQUARE_LOWER, HSV_WHITE_SQUARE_UPPER)
    black_color_mask = ColorDetector.get_color_mask(wrapped, HSV_BLACK_SQUARE_LOWER, HSV_BLACK_SQUARE_UPPER)
    cv2.imshow("White Color Detector", white_color_mask)
    cv2.imshow("Black Color Detector", black_color_mask)

# Show results
cv2.imshow('Corners and Lines',image)
cv2.imshow('Chessboard',wrapped)

# De-allocate any associated memory usage   
if cv2.waitKey(0) & 0xff == 27:  
    cv2.destroyAllWindows()  