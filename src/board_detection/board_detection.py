"""
Board Detection
@file           board-detection.py
@description    This file contains all necessary functions to
                extract a board game (chess or checkers board)
                of an image
@author         callFEELD
@version        0.1
"""

# Imports
import cv2              # for general image processing
import numpy as np      # for math operations


from config import DEBUG,\
    HSV_WHITE_SQUARE_LOWER, HSV_WHITE_SQUARE_UPPER, \
    HSV_BLACK_SQUARE_LOWER, HSV_BLACK_SQUARE_UPPER, \
    SQUARE_COLOR_THRESHOLD

from src import ColorDetector
from src.CheckersBoard import SquareColor, Square


def find_chessboard_corners(image, chessboard_size):
    """Finding chessboard corners inside an image.
    This function is using the opencv findChessboardCorners
    function.

    Arguments:
        image {cv2 image} -- opencv image
        chessboard_size {tuple} -- size of the chessboard example: (7, 7)
        for a 7x7 board

    Returns:
        list -- Ordered list of the corners. This function is returning the
        findChessboardCroners results.
    """
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # convert the image to a greyscale one
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # finding the chessboard corners using the buildin opencv function
    ret, corners = cv2.findChessboardCorners(gray, chessboard_size)

    # If found, add object points, image points (after refining them)
    if ret:
        cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        return corners
    return None


def estimate_next_corner(corners):
    """
    Estimating the next corner based on two or more corners.
    :param corners: list of corners (at least 2 corners)
    :return: the estimated next corner
    """

    # collect the offsets between the corners
    # with this information the estimated corner can be calculated
    x_offsets = []
    y_offsets = []
    for i in range(len(corners)-1):
        current_corner = corners[i][0]
        current_corner_x = current_corner[0]
        current_corner_y = current_corner[1]

        next_corner = corners[i+1][0]
        next_corner_x = next_corner[0]
        next_corner_y = next_corner[1]

        # calculate the offset between the current_corner and the next corner
        # and append the offset to the lists
        y_offsets.append(next_corner_y - current_corner_y)
        x_offsets.append(next_corner_x - current_corner_x)

    # only the offset between the corners is not precise enough
    # due to the 3d space of the corners and the image vanishing point
    # the offsets can increase/decrease between corners

    # With more than 2 corners there are more than 1 offsets.
    # Calculating the difference (delta) between the offsets,
    # will further estimate if the offsets will increase/decrease.
    # This increases the percision.
    x_delta = x_offsets[0] / x_offsets[-1]
    y_delta = y_offsets[0] / y_offsets[-1]

    first_corner_x = corners[0][0][0]
    first_corner_y = corners[0][0][1]

    return [first_corner_x - x_offsets[0] * x_delta, first_corner_y - y_offsets[0] * y_delta]


def estimate_chessboard8x8_corners(corners, display_points=False, image=None):
    """
    estimate the chessboard corners based on previous detected
    corners of the cv2.findChessboardCorners() function
    :param corners: cv2 findChessboardCorners (those are in order)
    """
    # NOTE: the coloring scheme is based on the
    # cv2.drawChessboardCorners colors

    # Estimate the 8 points based of the chessboard top left, top right
    # and bottom left and bottom right.
    front_pink = estimate_next_corner([corners[-1], corners[-2], corners[-3]])
    back_pink = estimate_next_corner([corners[-7], corners[-6], corners[-5]])

    front_red = estimate_next_corner(corners[0:3])
    back_red = estimate_next_corner([corners[6], corners[5], corners[4]])

    red_orange1 = estimate_next_corner([corners[0], corners[7], corners[14]])
    red_orange2 = estimate_next_corner([corners[6], corners[13], corners[20]])

    pink_blue1 = estimate_next_corner([corners[-1], corners[-8], corners[-15]])
    pink_blue2 = estimate_next_corner([corners[-7], corners[-14], corners[-21]])

    # get the intersections of the 8 points and therefore get the top left,
    # top right and bottom left and bottom right corners
    red_intersection1 = get_intersect(back_red, front_pink, red_orange1, red_orange2, integer=True)
    red_intersection2 = get_intersect(front_red, back_pink, red_orange1, red_orange2, integer=True)
    pink_intersection1 = get_intersect(back_red, front_pink, pink_blue1, pink_blue2, integer=True)
    pink_intersection2 = get_intersect(front_red, back_pink, pink_blue1, pink_blue2, integer=True)

    if display_points:
        # display the 8 points
        cv2.circle(image, (front_pink[0], front_pink[1]), 3, 255, -1)
        cv2.circle(image, (back_pink[0], back_pink[1]), 3, 255, -1)
        cv2.circle(image, (front_red[0], front_red[1]), 3, 255, -1)
        cv2.circle(image, (back_red[0], back_red[1]), 3, 255, -1)
        cv2.circle(image, (red_orange1[0], red_orange1[1]), 3, 255, -1)
        cv2.circle(image, (red_orange2[0], red_orange2[1]), 3, 255, -1)
        cv2.circle(image, (pink_blue1[0], pink_blue1[1]), 3, 255, -1)
        cv2.circle(image, (pink_blue2[0], pink_blue2[1]), 3, 255, -1)

        # display intersection points
        cv2.circle(image, (int(red_intersection1[0]), int(red_intersection1[1])), 3, (255,255,255), -1)
        cv2.circle(image, (int(red_intersection2[0]), int(red_intersection2[1])), 3, (255,255,255), -1)
        cv2.circle(image, (int(pink_intersection1[0]), int(pink_intersection1[1])), 3, (255,255,255), -1)
        cv2.circle(image, (int(pink_intersection2[0]), int(pink_intersection2[1])), 3, (255,255,255), -1)

    return [red_intersection1, red_intersection2, pink_intersection1, pink_intersection2]


def get_intersect(a1, a2, b1, b2, integer=False):
    """
    Returns the point of intersection of the lines passing
    through a2,a1 and b2,b1.
    a1: [x, y] a point on the first line
    a2: [x, y] another point on the first line
    b1: [x, y] a point on the second line
    b2: [x, y] another point on the second line
    """
    s = np.vstack([a1, a2, b1, b2])        # s for stacked
    h = np.hstack((s, np.ones((4, 1))))  # h for homogeneous
    l1 = np.cross(h[0], h[1])           # get first line
    l2 = np.cross(h[2], h[3])           # get second line
    x, y, z = np.cross(l1, l2)          # point of intersection
    if z == 0:                          # lines are parallel
        return (float('inf'), float('inf'))

    if integer:
        return [int(x/z), int(y/z)]
    return (x/z, y/z)


def get_chessboard_perspective(image, pts):
    # copied from https://www.pyimagesearch.com/2014/05/05/building-pokedex-python-opencv-perspective-warping-step-5-6/

    rect = np.zeros((4, 2), dtype="float32")

    pts = np.array(pts)
    # the top-left point has the smallest sum whereas the
    # bottom-right has the largest sum
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    # compute the difference between the points -- the top-right
    # will have the minumum difference and the bottom-left will
    # have the maximum difference
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    """
    rect[0] = pts[3]
    # bottom right
    rect[2] = pts[0]
    # top right
    rect[1] = pts[1]
    rect[3] = pts[2]
    """

    # now that we have our rectangle of points, let's compute
    # the width of our new image
    (tl, tr, br, bl) = rect
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))

    # ...and now for the height of our new image
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))

    # take the maximum of the width and height values to reach
    # our final dimensions
    maxWidth = max(int(widthA), int(widthB))
    maxHeight = max(int(heightA), int(heightB))

    # get the highest values
    highest_value = max(maxWidth, maxHeight)

    # construct our destination points which will be used to
    # map the screen to a top-down, "birds eye" view
    dst = np.array([
        [0, 0],
        [highest_value - 1, 0],
        [highest_value - 1, highest_value - 1],
        [0, highest_value - 1]], dtype="float32")

    # calculate the perspective transform matrix and warp
    # the perspective to grab the screen
    M = cv2.getPerspectiveTransform(rect, dst)
    return cv2.warpPerspective(image, M, (highest_value, highest_value))


def get_chessboard_squares(chessboard_perspective, size=(8, 8)):
    # retrieve the heigth and with information
    heigth, width, _ = chessboard_perspective.shape

    white_color_mask = ColorDetector.get_color_mask(chessboard_perspective,
                                                    HSV_WHITE_SQUARE_LOWER,
                                                    HSV_WHITE_SQUARE_UPPER)

    black_color_mask = ColorDetector.get_color_mask(chessboard_perspective,
                                                    HSV_BLACK_SQUARE_LOWER,
                                                    HSV_BLACK_SQUARE_UPPER)

    squares = []

    # split the image into the individual squares based of the size
    y, x = 0, 0
    for i in range(size[0]):
        x = 0
        for j in range(size[1]):
            # current square heigth and width
            square_h = int(heigth * (i+1)/8)
            square_w = int(width * (j+1)/8)

            # detect if the square is black or white
            isWhite = ColorDetector.has_area_color(
                white_color_mask[y:square_h, x:square_w],
                SQUARE_COLOR_THRESHOLD)
            isBlack = ColorDetector.has_area_color(
                black_color_mask[y:square_h, x:square_w],
                SQUARE_COLOR_THRESHOLD)

            # only black was detected
            if isBlack and not isWhite:
                squares.append(
                    Square(color=SquareColor.BLACK)
                )
            # only white was detected
            elif not isBlack and isWhite:
                squares.append(
                    Square(color=SquareColor.WHITE)
                )
            # both color were detected or none
            else:
                squares.append(
                    Square(color=SquareColor.UNDEFINED)
                )

            if DEBUG:
                cv2.imshow("Undefined square", chessboard_perspective[y:square_h, x:square_w])
                cv2.imshow("Undefined square white", white_color_mask[y:square_h, x:square_w])
                cv2.imshow("Undefined square black", black_color_mask[y:square_h, x:square_w])

                if cv2.waitKey(0) & 0xff == 27:
                        cv2.destroyAllWindows()
            x = square_w
        y = square_h

    return squares
