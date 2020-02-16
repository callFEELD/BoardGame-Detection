from src.board_detection import board_detection as bd


class NoBoardDetected(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, "Could not identify a 7x7 grid from \
            the opencv findChessboardCorners function.")


class BoardDetector:
    def __init__(self, image=None):
        self.set_image(image)
        self.corners = None
        self.board_corners = None
        self.perspective = None
        self.board_squares = None

    def get_perspective(self):
        return self.perspective

    def get_board_squares(self):
        return self.board_squares

    def set_image(self, image):
        self.image = image

    def detect_board(self):
        self.corners = bd.find_chessboard_corners(self.image, (7, 7))
        if self.corners is None:
            raise NoBoardDetected
        else:
            self.board_corners = bd.estimate_chessboard8x8_corners(
                self.corners, image=self.image)
            self.perspective = bd.get_chessboard_perspective(
                self.image, self.board_corners)
            self.board_squares = bd.get_chessboard_squares(
                self.perspective, size=(8, 8))
