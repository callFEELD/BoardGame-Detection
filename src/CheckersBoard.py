"""
Class of the Checkers Board interface
@file           board-detection.py
@description    This file contains all necessary classes for
                the checkerboard
@author         callFEELD
@version        0.1
"""


class CheckersState:
    """
    enum of the possible states
    """
    EMPTY = 0
    BLACK_MAN = 1
    BLACK_KING = 2
    WHITE_MAN = -1
    WHITE_KING = -2


class CheckerBoardSquare:
    """
    enum of checkr board square colors
    """
    BLACK_SQUARE = 1
    WHITE_SQUARE = -1
    UNDEFINED = 0
