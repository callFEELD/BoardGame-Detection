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
from config import DEBUG
from src.algo import grid_detection as gd

from src import ColorDetector
from config import HSV_BLACK_FIGURE_LOWER, HSV_BLACK_FIGURE_UPPER, \
    HSV_WHITE_FIGURE_LOWER, HSV_WHITE_FIGURE_UPPER

import cv2
import numpy as np

RESIZE_FACTOR = 6

file_name = "data/20200228_181947.jpg"

# read the image and make it smaller
image = cv2.imread(file_name)
image = cv2.resize(image, (int(4032/RESIZE_FACTOR), int(2268/RESIZE_FACTOR)))
oimage = image.copy()

# finding the chessboard inside an image
corners = bd.find_chessboard_corners(image, (7, 7))

# check if there are actuall chessboard corners
if corners is not None:
    if DEBUG:
        cv2.drawChessboardCorners(image, (7, 7), corners, 1)

    # estimate the missing chessboard corners
    board_corners = bd.estimate_chessboard8x8_corners(corners,
                                                      display_points=True,
                                                      image=image)

    # get only the chessboard perspective
    wrapped = bd.get_chessboard_perspective(oimage, board_corners)

    # get the individual squares of the chessboard
    squares = bd.get_chessboard_squares(wrapped, size=(8, 8))

    """
    for pos, square in enumerate(squares):
        if int(pos / 8) == 0:
            print(f"| {square.get_color()}", end='')
        else:
            print(f"| {square.get_color()}", end='')
    """

    cv2.imshow('Chessboard', wrapped)


eckpunkte = []


# mouse callback function
def mouse_callback(event,x,y,flags,param):
    global eckpunkte
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(eckpunkte) < 4:
            eckpunkte.append([x, y])
        else:
            eckpunkte = []
            eckpunkte.append([x, y])
        print(x, y)
        print(eckpunkte)

        if len(eckpunkte) == 4:
            wrapped = bd.get_chessboard_perspective(cimage, eckpunkte)
            cv2.imshow('Chessboard', wrapped)
            board = bd.get_chessboard_squares(wrapped)
            print(board)
            cv2.imwrite("wrapped.png", wrapped)

            black = ColorDetector.get_color_mask(wrapped,
                                                    HSV_BLACK_FIGURE_LOWER,
                                                    HSV_BLACK_FIGURE_UPPER)
            white = ColorDetector.get_color_mask(wrapped,
                                                    HSV_WHITE_FIGURE_LOWER,
                                                    HSV_WHITE_FIGURE_UPPER)
            cv2.imshow("black", black)
            cv2.imshow("white", white)




cimage = image.copy()
gray = cv2.cvtColor(cimage, cv2.COLOR_BGR2GRAY)
corners = bd.get_corners(cimage)


points = []
for corner in corners:
    points.append(corner[0])

for point in points:
    cv2.circle(image, (point[0], point[1]), 3, (255, 255, 0), -1)


NMBR = 72
cv2.circle(image, (points[NMBR][0], points[NMBR][1]), 3, (255, 255, 255), -1)
close_points = gd.find_close_points(points[NMBR], points)

distances = gd.get_distance_from_point(points[NMBR], points)
distances = sorted(distances)

for point in close_points:
    cv2.circle(image, (point[0], point[1]), 3, 255, -1)


# Show results
cv2.imshow('image', image)
cv2.namedWindow('image',cv2.WINDOW_NORMAL) # Can be resized
cv2.setMouseCallback('image', mouse_callback) #Mouse callback


# De-allocate any associated memory usage
if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()
