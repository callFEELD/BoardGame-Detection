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
fname = "data/20191113_134320.jpg" # top down view
#fname = "data/20191113_134334.jpg"
#fname = "data/20191113_134324.jpg"
#fname = "data/20191113_134307.jpg"


# image loading and preperation
image = cv2.imread(fname)
image = cv2.resize(image,(int(4032/4), int(2268/4)))
oimage = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# finding chessboard
corners = bd.find_chessboard(gray, (7,7))
if corners is not None:
    cv2.drawChessboardCorners(image, (7,7), corners, 1)

    # estimating the next corners that are missing (due to a 9x9 board)
    new_corner = bd.estimate_next_corner(corners[0:2])
    front_red = new_corner
    cv2.circle(image,(new_corner[0],new_corner[1]),3,255,-1)

    new_corner = bd.estimate_next_corner([corners[-1], corners[-2]])
    front_pink = new_corner
    cv2.circle(image,(new_corner[0],new_corner[1]),3,255,-1)


    new_corner = bd.estimate_next_corner([corners[0], corners[7]])
    red_orange1 = new_corner
    cv2.circle(image,(new_corner[0],new_corner[1]),3,255,-1)

    new_corner = bd.estimate_next_corner([corners[-1], corners[-8]])
    pink_blue1 = new_corner
    cv2.circle(image,(new_corner[0],new_corner[1]),3,255,-1)

    new_corner = bd.estimate_next_corner([corners[6], corners[5]])
    back_red = new_corner
    cv2.circle(image,(new_corner[0],new_corner[1]),3,255,-1)

    new_corner = bd.estimate_next_corner([corners[6], corners[13]])
    red_orange2 = new_corner
    cv2.circle(image,(new_corner[0],new_corner[1]),3,255,-1)

    new_corner = bd.estimate_next_corner([corners[-7], corners[-14]])
    pink_blue2 = new_corner
    cv2.circle(image,(new_corner[0],new_corner[1]),3,255,-1)

    new_corner = bd.estimate_next_corner([corners[-7], corners[-6]])
    back_pink = new_corner
    cv2.circle(image,(new_corner[0],new_corner[1]),3,255,-1)

    # build lines from the corners and get the intersection
    intersect1 = bd.get_intersect(front_red, back_pink, red_orange1, red_orange2, integer=True)
    cv2.circle(image,(int(intersect1[0]),int(intersect1[1])),3,(255,255,255),-1)

    intersect2 = bd.get_intersect(front_red, back_pink, pink_blue1, pink_blue2, integer=True)
    cv2.circle(image,(int(intersect2[0]),int(intersect2[1])),3,(255,255,255),-1)

    intersect3 = bd.get_intersect(back_red, front_pink, red_orange1, red_orange2, integer=True)
    cv2.circle(image,(int(intersect3[0]),int(intersect3[1])),3,(255,255,255),-1)

    intersect4 = bd.get_intersect(back_red, front_pink, pink_blue1, pink_blue2, integer=True)
    cv2.circle(image,(int(intersect4[0]),int(intersect4[1])),3,(255,255,255),-1)

    wrapped = bd.get_chessboard(oimage, [intersect1,intersect2,intersect3,intersect4])

# Show results
cv2.imshow('Corners and Lines',image)
cv2.imshow('Chessboard',wrapped)

# De-allocate any associated memory usage   
if cv2.waitKey(0) & 0xff == 27:  
    cv2.destroyAllWindows()  