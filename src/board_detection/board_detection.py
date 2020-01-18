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


# detection of coners 
def get_corners(image):
    MAX_CORNERS:int = 1000
    QUALITY_LEVEL:float = 0.001
    MIN_DISTANCE:int = 10
    return cv2.goodFeaturesToTrack(image, MAX_CORNERS, QUALITY_LEVEL, MIN_DISTANCE, useHarrisDetector=True)


# getting lines based on Hough Lines
def get_lines(image):
    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 80  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 100  # minimum number of pixels making up a line
    max_line_gap = 100000  # maximum gap in pixels between connectable line segments
    lines = cv2.HoughLinesP(image, rho, theta, threshold, np.array([]),
                        min_line_length, max_line_gap)
    
    return lines