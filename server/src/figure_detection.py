import cv2
import numpy as np
import math


def find_circles(image, rho=1, mindist=40, param1=150, param2=15, minRadius=0, maxRadius=30):
    """Find circles inside an image based on HoughCricle

    Arguments:
        image {[type]} -- [description]

    Keyword Arguments:
        param1 {int} -- cv2.HoughCircles parameter (default: {150})
        param2 {int} -- cv2.HoughCircles parameter (default: {15})
        minRadius {int} -- cv2.HoughCircles parameter (default: {0})
        maxRadius {int} -- cv2.HoughCircles parameter (default: {30})

    Returns:
        np.array -- List of Circles, uint16 rounded to integer
                    Each formatted the following way:
                        circle =[x_pos, y_pos, radius]
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(
        gray, cv2.HOUGH_GRADIENT, rho, mindist,
        param1=param1, param2=param2, minRadius=minRadius,
        maxRadius=maxRadius
    )

    return np.uint16(np.around(circles))


def get_circle_img(image, r, x, y):
    """Get a rectangular image crop of the circle.
    This crop is the biggest square inside the circle.

    Arguments:
        image {np.array} -- OpenCV image which should be cropped
        r {int} -- radius of the circle
        x {int} -- x pos of the circle
        y {int} -- y pos of the circle

    Returns:
        np.array -- corpped opencv image
    """
    radian = 45 * math.pi / 180
    delta = int(math.sin(radian) * r)

    return image[y-delta:y+delta, x-delta:x+delta]
