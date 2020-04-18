from fastapi import APIRouter, HTTPException
import base64
import cv2
import pickle
import numpy as np

from src.GameBoardDetector import BoardDetector, FigureDetector


router = APIRouter()


@router.post('/analyse')
async def analyse_board(json_data: dict):
    image = json_data["image"]
    image = base64.b64decode(image)
    image = pickle.loads(image)
    image = np.array(image)
    options = json_data["options"]

    gbd = BoardDetector()
    gfd = FigureDetector()

    if options is not None:
        gbd.update_options(options["boarddetector"])
        gfd.update_options(options["figuredetector"])

    board_perspective = gbd.find_board(image)
    gbd.show_debug_layers()

    pieces = None
    if board_perspective is not None:
        pieces = gfd.find_pieces(board_perspective)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return pieces
    else:
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return {}
