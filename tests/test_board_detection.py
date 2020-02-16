import sys
import os
import unittest
import cv2
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/..")


from src.board_detection.BoardDetector import BoardDetector


class TestBoardDetection(unittest.TestCase):
    def test_20191113_134305(self):
        file_name = "data/20191113_134305.jpg"
        board = [0, 1, 0, 1, 0, 1, 0, 1,
                 1, 0, 1, 0, 1, 0, 1, 0,
                 0, 1, 0, 1, 0, 1, 0, 1,
                 1, 0, 1, 0, 1, 0, 1, 0,
                 0, 1, 0, 1, 0, 1, 0, 1,
                 1, 0, 1, 0, 1, 0, 1, 0,
                 0, 1, 0, 1, 0, 1, 0, 1,
                 1, 0, 1, 0, 1, 0, 1, 0]

        image = cv2.imread(file_name)
        image = cv2.resize(image, (int(4032/4), int(2268/4)))

        bd = BoardDetector(image=image)
        bd.detect_board()

        self.assertEqual(bd.get_board_squares(), board)

    def test_20191113_134311(self):
        file_name = "data/20191113_134311.jpg"
        board = [0, 1, 0, 1, 0, 1, 0, 1,
                 1, 0, 1, 0, 1, 0, 1, 0,
                 0, 1, 0, 1, 0, 1, 0, 1,
                 1, 0, 1, 0, 1, 0, 1, 0,
                 0, 1, 0, 1, 0, 1, 0, 1,
                 1, 0, 1, 0, 1, 0, 1, 0,
                 0, 1, 0, 1, 0, 1, 0, 1,
                 1, 0, 1, 0, 1, 0, 1, 0]

        image = cv2.imread(file_name)
        image = cv2.resize(image, (int(4032/4), int(2268/4)))

        bd = BoardDetector(image=image)
        bd.detect_board()

        self.assertEqual(bd.get_board_squares(), board)

    def test_20191113_134320(self):
        file_name = "data/20191113_134320.jpg"
        board = [1, 0, 1, 0, 1, 0, 1, 0,
                 0, 1, 0, 1, 0, 1, 0, 1,
                 1, 0, 1, 0, 1, 0, 1, 0,
                 0, 1, 0, 1, 0, 1, 0, 1,
                 1, 0, 1, 0, 1, 0, 1, 0,
                 0, 1, 0, 1, 0, 1, 0, 1,
                 1, 0, 1, 0, 1, 0, 1, 0,
                 0, 1, 0, 1, 0, 1, 0, 1]

        image = cv2.imread(file_name)
        image = cv2.resize(image, (int(4032/4), int(2268/4)))

        bd = BoardDetector(image=image)
        bd.detect_board()

        self.assertEqual(bd.get_board_squares(), board)

    def test_20191113_134340(self):
        file_name = "data/20191113_134340.jpg"
        board = [0, 1, 0, 1, 0, 1, 0, 1,
                 1, 0, 1, 0, 1, 0, 1, 0,
                 0, 1, 0, 1, 0, 1, 0, 1,
                 1, 0, 1, 0, 1, 0, 1, 0,
                 0, 1, 0, 1, 0, 1, 0, 1,
                 1, 0, 1, 0, 1, 0, 1, 0,
                 0, 1, 0, 1, 0, 1, 0, 1,
                 1, 0, 1, 0, 1, 0, 1, 0]

        image = cv2.imread(file_name)
        image = cv2.resize(image, (int(4032/4), int(2268/4)))

        bd = BoardDetector(image=cv2.imread(file_name))
        bd.detect_board()

        self.assertEqual(bd.get_board_squares(), board)

    def test_20191113_134324(self):
        file_name = "data/20191113_134324.jpg"
        board = [1, 0, 1, 0, 1, 0, 1, 0,
                 0, 1, 0, 1, 0, 1, 0, 1,
                 1, 0, 1, 0, 1, 0, 1, 0,
                 0, 1, 0, 1, 0, 1, 0, 1,
                 1, 0, 1, 0, 1, 0, 1, 0,
                 0, 1, 0, 1, 0, 1, 0, 1,
                 1, 0, 1, 0, 1, 0, 1, 0,
                 0, 1, 0, 1, 0, 1, 0, 1]

        image = cv2.imread(file_name)
        image = cv2.resize(image, (int(4032/4), int(2268/4)))

        bd = BoardDetector(image=image)
        bd.detect_board()

        self.assertEqual(bd.get_board_squares(), board)

    def test_20191113_134341(self):
        file_name = "data/20191113_134341.jpg"
        board = [0, 1, 0, 1, 0, 1, 0, 1,
                 1, 0, 1, 0, 1, 0, 1, 0,
                 0, 1, 0, 1, 0, 1, 0, 1,
                 1, 0, 1, 0, 1, 0, 1, 0,
                 0, 1, 0, 1, 0, 1, 0, 1,
                 1, 0, 1, 0, 1, 0, 1, 0,
                 0, 1, 0, 1, 0, 1, 0, 1,
                 1, 0, 1, 0, 1, 0, 1, 0]

        image = cv2.imread(file_name)
        image = cv2.resize(image, (int(4032/4), int(2268/4)))

        bd = BoardDetector(image=image)
        bd.detect_board()

        self.assertEqual(bd.get_board_squares(), board)


if __name__ == '__main__':
    unittest.main()
