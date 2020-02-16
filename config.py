"""This file contains necessary information for production
"""

import numpy as np


"""Board Square Colors
"""
# White square colors
HSV_WHITE_SQUARE_LOWER: np.array(size=(1, 3)) = np.array([0, 0, 200])
HSV_WHITE_SQUARE_UPPER: np.array(size=(1, 3)) = np.array([180, 255, 255])

# black square colors
HSV_BLACK_SQUARE_LOWER: np.array(size=(1, 3)) = np.array([0, 0, 0])
HSV_BLACK_SQUARE_UPPER: np.array(size=(1, 3)) = np.array([255, 255, 190])
