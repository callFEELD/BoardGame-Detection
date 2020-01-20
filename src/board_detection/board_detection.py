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


def find_chessboard(image, chessboard_size):
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    ret, corners = cv2.findChessboardCorners(image, chessboard_size)
    #    If found, add object points, image points (after refining them)
    if ret == True:
        cv2.cornerSubPix(image, corners, (11,11), (-1,-1), criteria)
        return corners
    return None

def estimate_next_corner(corners):
    # first get the first corner
    corner1 = corners[0][0]
    x1 = corner1[0]
    y1 = corner1[1]

    # get the corner before 
    corner2 = corners[1][0]
    x2 = corner2[0]
    y2 = corner2[1]
    
    y_offset = y2 - y1
    x_offset = x2 - x1
    
    return [x1-x_offset, y1-y_offset]

def get_intersect(a1, a2, b1, b2):
    """ 
    Returns the point of intersection of the lines passing through a2,a1 and b2,b1.
    a1: [x, y] a point on the first line
    a2: [x, y] another point on the first line
    b1: [x, y] a point on the second line
    b2: [x, y] another point on the second line
    """
    s = np.vstack([a1,a2,b1,b2])        # s for stacked
    h = np.hstack((s, np.ones((4, 1)))) # h for homogeneous
    l1 = np.cross(h[0], h[1])           # get first line
    l2 = np.cross(h[2], h[3])           # get second line
    x, y, z = np.cross(l1, l2)          # point of intersection
    if z == 0:                          # lines are parallel
        return (float('inf'), float('inf'))
    return (x/z, y/z)

# For self written chessboard finder

# detection of coners 
def get_corners(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    MAX_CORNERS:int = 1000
    QUALITY_LEVEL:float = 0.001
    MIN_DISTANCE:int = 15
    return cv2.goodFeaturesToTrack(gray, MAX_CORNERS, QUALITY_LEVEL, MIN_DISTANCE, useHarrisDetector=True)

# getting lines based on Hough Lines
def get_lines(image):
    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 75  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 100  # minimum number of pixels making up a line
    max_line_gap = 100000  # maximum gap in pixels between connectable line segments
    lines = cv2.HoughLinesP(image, rho, theta, threshold, np.array([]),
                        min_line_length, max_line_gap)
    
    return lines

def get_intersections(lines):
    ret_intersections = []
    if lines is not None:
        for line in lines:
            for x1,y1,x2,y2 in line:
                for nline in lines:
                    for nx1,ny1,nx2,ny2 in nline:
                        px, py = get_intersect([x1, y1], [x2, y2], [nx1, ny1], [nx2, ny2])

                        if px != float('inf') and py != float('inf'):
                            ret_intersections.append([px, py])
    
    return ret_intersections

def is_close_to(point1, point2):
    diff = 4 # 4pixels

    p1x, p1y = point1
    p2x, p2y = point2

    if abs(p1x - p2x) <= diff and abs(p1y - p2y) <= diff:
        return True
    return False

def find_lines_with_corners(img, lines, corners):
    max_diff = 2 # 4 pixels
    """
    # get the x positions of all corners
    x_corners = [corner.ravel()[0] for corner in corners]
    y_corners = [corner.ravel()[0] for corner in corners]

    # get possible y's of the y corners based on the linera function of the line
    possible_ys = np.interp(x_corners, [x1, x2], [y1, y2])
    """

    ret_lines = []
    if lines is not None:
        for line in lines:
            for x1,y1,x2,y2 in line:

                xp = [x1, x2]
                fp = [y1, y2]

                amount = 0
                for corner in corners:
                    x,y = corner

                    # check if corner is on the line
                    ty = np.interp(x, xp, fp)

                    if abs(int(ty)-y) <= max_diff:
                        cv2.circle(img,(x,int(ty)),1,(255,255,0),-1)
                        amount += 1

                if amount >= 5: #and amount <= 12:
                    ret_lines.append(line)
    return ret_lines
