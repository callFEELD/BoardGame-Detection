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
from src.CheckersBoard import SquareColor


def find_lines(image, rho, theta, threshold):
    """Finding lines based on a hough transformation for lines

    Arguments:
        image {[type]} -- [description]
        rho {[type]} -- [description]
        theta {[type]} -- [description]
        threshold {[type]} -- [description]

    Returns:
        cv2.HoughLines --  the found lines
    """
    kernel = np.ones((3, 3), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    return cv2.HoughLines(image, rho, theta, threshold)


def filter_lines(lines, rho_threshold, theta_threshold):
    """Filtering lines which are close to each other

    Arguments:
        lines {cv2.HoughLines} -- Found cv2.HoughLines
        rho_threshold {[type]} -- [description]
        theta_threshold {[type]} -- [description]

    Returns:
        cv2.HoughLines -- filtered hough lines
    """
    if lines is None:
        return None

    similar_lines = {i : [] for i in range(len(lines))}

    for i in range(len(lines)):
        for j in range(len(lines)):
            if i == j:
                continue

            rho_i,theta_i = lines[i][0]
            rho_j,theta_j = lines[j][0]

            if abs(rho_i - rho_j) < rho_threshold and abs(theta_i - theta_j) < theta_threshold:
                similar_lines[i].append(j)

    indices = [i for i in range(len(lines))]
    indices.sort(key=lambda x : len(similar_lines[x]))

    # line flags is the base for the filtering
    line_flags = len(lines)*[True]
    for i in range(len(lines) - 1):
        if not line_flags[indices[i]]: # if we already disregarded the ith element in the ordered list then we don't care (we will not delete anything based on it and we will never reconsider using this line again)
            continue

        for j in range(i + 1, len(lines)): # we are only considering those elements that had less similar line
            if not line_flags[indices[j]]: # and only if we have not disregarded them already
                continue

            rho_i,theta_i = lines[indices[i]][0]
            rho_j,theta_j = lines[indices[j]][0]
            if abs(rho_i - rho_j) < rho_threshold and abs(theta_i - theta_j) < theta_threshold:
                line_flags[indices[j]] = False

    filtered_lines = []
    for i in range(len(lines)): # filtering
        if line_flags[i]:
            filtered_lines.append(lines[i])
    return filtered_lines


def find_corners(image, max_corners, quality_level, min_distance):
    """Finds corners inside an image based on cv2.goodFeaturesToTrack with Harris

    Arguments:
        image {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    return cv2.goodFeaturesToTrack(
        gray, max_corners, quality_level, min_distance, useHarrisDetector=True
    )


def divide_chessboard(chessboard_perspective, size=(8, 8)):
    width = chessboard_perspective.shape[0]
    height = chessboard_perspective.shape[1]
    x_step = width/size[0]
    y_step = height/size[1]

    images = []
    positions = []
    for x in range(size[0]):
        row = []
        row_pos = []
        for y in range(size[1]):
            row.append(
                chessboard_perspective[int(y_step*y):int(y_step*(y+1)), int(x_step*x):int(x_step*(x+1))]
            )
            row_pos.append({"x":[int(y_step*y), int(y_step*(y+1))], "y": [int(x_step*x), int(x_step*(x+1))]})
        images.append(row)
        positions.append(row_pos)
    return images, positions



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

def get_intersections(lines):
    ret_obj = []
    """
    ret_obj = [
        {
            line: LINE_INDEX,
            intersections: [
                {
                    line: LINE_INDEX,
                    position: [x, y]
                }
            ]
        }
    ]
    """
    if lines is not None:
        for i, line in enumerate(lines):
            line_intersections = []
            x1, y1, x2, y2 = line
            for j, nline in enumerate(lines):
                if j==i:
                    continue
                nx1, ny1, nx2, ny2 = nline
                px, py = get_intersect([x1, y1], [x2, y2], [nx1, ny1], [nx2, ny2])

                if px != float('inf') and py != float('inf'):
                    line_intersections.append({
                        "line": j,
                        "position": [px, py]
                    })

            ret_obj.append(
                {
                    "line": i,
                    "intersections": line_intersections
                }
            )

    return ret_obj


def filter_intersections(intersections, image, display=False):
    height, width, _ = image.shape
    # filter intersections that are not in the image
    for i, line in enumerate(intersections):
        to_be_removed = []
        for intersec in line["intersections"]:
            if intersec["position"][0] < 0 or intersec["position"][1] < 0 or intersec["position"][0] > width or intersec["position"][1] > height:
                to_be_removed.append(intersec)
            else:
                if display:
                    cv2.circle(image, (int(intersec["position"][0]), int(intersec["position"][1])), 5, (255, 255, 255))
        for remove in to_be_removed:
            intersections[i]["intersections"].remove(remove)


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



def is_close_to(point1, point2, radian=4):
    p1x, p1y = point1
    p2x, p2y = point2

    if abs(p1x - p2x) <= radian and abs(p1y - p2y) <= radian:
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
