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
    WHITE_SQUARE = 0


class CheckersBoard:
    """
    Example of a 4x4 Checkers Board
    |------------|
    | 0  1  0  1 | <- Black Figure start row
    | 0  0  0  0 |
    | 0  0  0  0 |
    |-1  0 -1  0 | <- White Figure start row
    |------------|
    """
    # Board size --> SIZExSIZE Board
    SIZE = 8

    # The board itself
    board = []

    def __init__(self):
        self._create_empty_board()

    def _create_empty_board(self):
        """
        This method creates the empty state of the board, without figures
        """
        self.board = []
        for _ in range(self.SIZE):
            row = []
            for _ in range(self.SIZE):
                row.append(CheckersState.EMPTY)
            self.board.append(row)

    def reset(self):
        """
        This resets the board to the beginning (empty) state with no figures
        """
        self.board = []
        self._create_empty_board()

    def get(self):
        """
        This method returns the board
        """
        return self.board
