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


class SquareColor:
    """
    enum of checkr board square colors
    """
    BLACK = 1
    WHITE = 0
    UNDEFINED = -1


class Square:
    def __init__(self, color=SquareColor.WHITE):
        self.color: SquareColor = color

    def get_color(self):
        return self.color

    def set_color(self, color: SquareColor):
        self.color = color
