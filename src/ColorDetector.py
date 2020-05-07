"""
Color Detector
@file           board-detection.py
@description    This file contains all necessary functions to
                find color inside an image
@author         callFEELD
@version        0.1
"""

import cv2
import numpy as np

KERNEL = np.ones((3, 3), np.uint8)


def get_color_mask(image, hsv_color_lower, hsv_color_upper):
    # converting to HUE color space for color detection
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # scan for the color in the range given
    color_mask = cv2.inRange(hsv_image, hsv_color_lower, hsv_color_upper)
    color_mask = cv2.morphologyEx(color_mask, cv2.MORPH_DILATE, KERNEL)
    color_mask = cv2.morphologyEx(color_mask, cv2.MORPH_ERODE, KERNEL)

    return color_mask


def has_area_color(color_mask, threshold):
    square_area = color_mask.shape[0] * color_mask.shape[1]

    if cv2.countNonZero(color_mask) >= square_area * threshold:
        return True
    return False


def threshold_mask(image, thresh, threshold_type=cv2.THRESH_BINARY):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    ret, threshold = cv2.threshold(gray, thresh, 255, threshold_type)
    return threshold