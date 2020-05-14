from .client import Client

from picamera import PiCamera
import time
from PIL import Image
import numpy as np


class PiClient(Client):
    filename: str = "piclient_capture.jpg"
    resolution: tuple = (1080, 1080)

    def __init__(self, url=None, token=None):
        super().__init__(url=url, token=token)
        self.init_picamera()

    def init_picamera(self):
        self.camera = PiCamera()
        self.camera.resolution = self.resolution
        self.camera.start_preview()
        time.sleep(2)

    def get_image(self):
        file = open(self.filename, 'wb')
        self.camera.capture(file)
        file.close()

        image = Image.open(self.filename)
        image = image.rotate(self.rotation)
        image = np.array(image)
        # Convert RGB to BGR
        return image[:, :, ::-1].copy()
