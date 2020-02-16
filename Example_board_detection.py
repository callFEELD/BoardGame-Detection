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
import time


DEBUG = True


fname = "data/20191113_134305.jpg"
fname = "data/20191113_134320.jpg"  # top down view
fname = "data/20191113_134334.jpg"
fname = "data/20191113_134324.jpg"
# fname = "data/20191113_134307.jpg"

start_time = time.time()
# image loading and preperation
image = cv2.imread(fname)
image = cv2.resize(image, (int(4032/4), int(2268/4)))
oimage = image.copy()

# finding the chessboard inside an image
corners = bd.find_chessboard_corners(image, (7, 7))
end_time = time.time()
print(end_time - start_time)

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

    print(squares)

print(time.time()-start_time)
# Show results
cv2.imshow('Corners and Lines', image)
cv2.imshow('Chessboard', wrapped)

# De-allocate any associated memory usage
if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()
