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

import cv2


file_name = "data/20191113_134324.jpg"

# read the image and make it smaller
image = cv2.imread(file_name)
image = cv2.resize(image, (int(4032/4), int(2268/4)))
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

    for pos, square in enumerate(squares):
        if int(pos / 8) == 0:
            print(f"| {square.get_color()}", end='')
        else:
            print(f"| {square.get_color()}", end='')

# Show results
cv2.imshow('Corners and Lines', image)
cv2.imshow('Chessboard', wrapped)

# De-allocate any associated memory usage
if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()
