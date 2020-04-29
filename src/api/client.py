import asyncio
from PIL import Image
import cv2
import numpy as np
import imutils
from aiohttp import ClientSession, ClientTimeout

from src.api.utils import img2str


class Client:
    rotation: int = 90
    url: str = None
    token: str = None
    timeout: int = 30
    headers: dict = None

    def __init__(self, url=None, token=None):
        self.set_url(url)
        self.set_token(token)

    def get_image(self):
        image = Image.open("Unbenannt.JPG")
        image = image.rotate(self.rotation)
        image = np.array(image)
        # Convert RGB to BGR
        return image[:, :, ::-1].copy()

    def set_token(self, token: str):
        self.token = token
        self.headers = {
            'X-authentication-token': self.token
        }

    def set_url(self, url: str):
        self.url = url

    async def _request(self, json):
        timeout = ClientTimeout(total=self.timeout)

        async with ClientSession(timeout=timeout) as session:
            # make a valid move
            async with session.post(self.url, headers=self.headers,
                                    json=json) as resp:
                assert resp.status == 200
                return await resp.json()

    def detect(self, options=None):
        # get the current image
        image = self.get_image()

        json = {
            "image": img2str(image),
            "options": options
        }

        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self._request(json))


class StreamClient(Client):
    stream_url: str = None

    def __init__(self, url=None, token=None, stream_url=None):
        super().__init__()
        self.set_stream_url(stream_url)

    def set_stream_url(self, stream_url):
        self.stream_url = stream_url

    def get_image(self):
        cap = cv2.VideoCapture(self.stream_url)
        while True:
            ret, frame = cap.read()
            if ret:
                return imutils.rotate(frame, self.rotation)
