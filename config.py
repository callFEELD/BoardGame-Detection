"""This file contains necessary information for production
"""

import numpy as np


DEBUG = False

"""Board Square Colors
"""
# White square colors
HSV_WHITE_SQUARE_LOWER: np.array = np.array([0, 0, 200])
HSV_WHITE_SQUARE_UPPER: np.array = np.array([180, 255, 255])

# black square colors
HSV_BLACK_SQUARE_LOWER: np.array = np.array([0, 0, 0])
HSV_BLACK_SQUARE_UPPER: np.array = np.array([255, 255, 190])

# Square color treshold
# At what percentage a square should be defined as black or white
SQUARE_COLOR_THRESHOLD: float = 0.5
