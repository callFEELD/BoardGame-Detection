"""
Example_BoardGame_Detection
@file           Example_BoardGame_Detection.py
@description    This file contains an example of how to use the
                game board detectors
@author         callFEELD
@version        0.1
"""

from src.GameBoardDetector import BoardDetector, FigureDetector
import cv2
import time


PI = "http://192.168.255.10:8000/stream.mjpg"


def get_img_from_pi():
    while True:
        cap = cv2.VideoCapture(PI)
        ret, frame = cap.read()
        if ret:
            img = frame
            cap.release()
            return img


def single_test():
    img = get_img_from_pi()
    # img = cv2.imread("data/20200228_181820.jpg")
    # height, width, _ = img.shape

    gbd = BoardDetector()
    gfd = FigureDetector()


    options = {
        "corners": {
            "maxcorners": 500,
            "qualitylevel": 0.001,
            "mindistance": 20
        }
    }
    gbd.update_options(options)

    start = time.time()
    board_perspective = gbd.find_board(img)
    gbd.show_debug_layers()
    if board_perspective is not None:
        pieces = gfd.find_pieces(board_perspective)
        gfd.show_debug_layers()
        print(pieces)
        print()

    print(f"Image analysing time: {int((time.time()-start)*1000)}ms")

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def videocapture_test():
    gbd = BoardDetector()
    gfd = FigureDetector()

    options = {
        "corners": {
            "maxcorners": 500,
            "qualitylevel": 0.001,
            "mindistance": 20
        }
    }

    gbd.update_options(options)

    cap = cv2.VideoCapture(PI)
    while True:
        ret, frame = cap.read()
        if ret:
            start = time.time()
            board_perspective = gbd.find_board(frame)
            gbd.show_debug_layers()
            if board_perspective is not None:
                pieces = gfd.find_pieces(board_perspective)
                gfd.show_debug_layers()
                print(pieces)
                print()

            print(f"Image analysing time: {int((time.time()-start)*1000)}ms")

            if cv2.waitKey(1) == 27:
                break


videocapture_test()
