from pydantic import BaseModel
from typing import Optional

class Options(BaseModel):
    boarddetector: dict
    figuredetector: dict

class Analyze(BaseModel):
    image: str
    options: Optional[Options]
