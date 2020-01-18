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

#fname = "data/20191113_134305.jpg"
#fname = "data/20191113_134320.jpg" # top down view
fname = "data/20191113_134334.jpg" 

# image loading and preperation
image = cv2.imread(fname)
image = cv2.resize(image,(int(4032/6), int(2268/6)))
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 200)

# detecting features
corners = bd.get_corners(gray)
lines = bd.get_lines(edges)

# adding the lines to the image
if lines is not None:
    # draw lines
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(image,(x1,y1),(x2,y2),(0,255,0),2)

# add the corners to the image
for corner in corners:
    x,y = corner.ravel()
    cv2.circle(image,(x,y),3,255,-1)

# Show results
cv2.imshow('Corners and Lines',image)
cv2.imshow('Edges',edges)
cv2.imshow('Gray',gray)

# De-allocate any associated memory usage   
if cv2.waitKey(0) & 0xff == 27:  
    cv2.destroyAllWindows()  