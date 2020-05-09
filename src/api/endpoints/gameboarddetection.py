import time
from fastapi import APIRouter, Response

from src.GameBoardDetector import BoardDetector, FigureDetector
from src.api.endpoints.models import Analyze
from src.api.utils import str2img, img2str

router = APIRouter()


@router.get('/ping')
async def ping_pong(response: Response):
    response.headers["X-Send-Time"] = str(time.time())
    return {}


@router.post('/analyse')
async def analyse_board(data: Analyze):
    image = str2img(data.image)
    options = data.options

    gbd = BoardDetector()
    gfd = FigureDetector()

    if options is not None:
        gbd.update_options(options.boarddetector)
        gfd.update_options(options.figuredetector)

    board_perspective = gbd.find_board(image)

    if board_perspective is not None:
        pieces = gfd.find_pieces(board_perspective)
        return pieces
    else:
        return None


@router.post('/debuganalyse')
async def debug_analyse_board(data: Analyze):
    image = str2img(data.image)
    options = data.options

    gbd = BoardDetector()
    gfd = FigureDetector()

    if options is not None:
        gbd.update_options(options.boarddetector)
        gfd.update_options(options.figuredetector)

    board_perspective = gbd.find_board(image)

    debug_layers = []
    for layer in gbd.layers:
        debug_layers.append({
            "name": layer["name"],
            "img": img2str(layer["image"])
        })

    if board_perspective is not None:
        pieces = gfd.find_pieces(board_perspective)
        for layer in gfd.layers:
            debug_layers.append({
                "name": layer["name"],
                "img": img2str(layer["image"])
            })

        return {
            "pieces": pieces,
            "debug": debug_layers
        }
    else:
        return {
            "pieces": None,
            "debug": debug_layers
        }
