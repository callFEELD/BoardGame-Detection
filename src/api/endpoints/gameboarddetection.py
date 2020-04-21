import base64
import pickle

import cv2
import numpy as np
import time
from fastapi import APIRouter, Response, HTTPException

from src.GameBoardDetector import BoardDetector, FigureDetector
from src.api.endpoints.models import Analyze

router = APIRouter()


@router.get('/ping')
async def ping_pong(response: Response):
    response.headers["X-Send-Time"] = str(time.time())
    return {}


@router.post('/analyse')
async def analyse_board(data: Analyze):
    image = data.image
    image = base64.b64decode(image)
    image = pickle.loads(image)
    image = np.array(image)
    options = data.options

    gbd = BoardDetector()
    gfd = FigureDetector()

    if options is not None:
        gbd.update_options(options.boarddetector)
        gfd.update_options(options.figuredetector)

    board_perspective = gbd.find_board(image)
    gbd.show_debug_layers()

    if board_perspective is not None:
        pieces = gfd.find_pieces(board_perspective)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return pieces
    else:
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        raise HTTPException(status_code=404, detail='The bord could not be found')
