"""
Chessboard finder (selfwritten)
@file           chessboard_finder.py
@description    tbd
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
fname = "data/20191113_134334.jpg"
fname = "data/20191113_134324.jpg"
#fname = "data/20191113_134307.jpg"


# image loading and preperation
image = cv2.imread(fname)

image = cv2.resize(image,(int(4032/6), int(2268/6)))

kernel = np.ones((5, 5),np.uint8)
image2 = cv2.GaussianBlur(image, (11,11), 0)


gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 0, 75)

# detecting features
corners = bd.get_corners(image)
lines = bd.get_lines(edges)

intersections = bd.get_intersections(lines)


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

filtered_points = []
for corner in corners:
    for intersection in intersections:
        x, y = corner.ravel()
        if bd.is_close_to(corner.ravel(), intersection):
            cv2.circle(image,(int(x),int(y)),2,(255,0,255),-1)
            filtered_points.append([x,y])

c_lines = bd.find_lines_with_corners(image, lines, filtered_points)


if c_lines is not None:
    # draw lines
    for line in c_lines:
        for x1,y1,x2,y2 in line:
            cv2.line(image,(x1,y1),(x2,y2),(255,255,255),2)

for intersection in intersections:
    x,y = intersection
    cv2.circle(image,(int(x),int(y)),2,(0,0,255),-1)

# Show results
cv2.imshow('Corners and Lines',image)