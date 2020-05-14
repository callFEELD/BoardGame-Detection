from .client import Client

import cv2
import imutils


class StreamClient(Client):
    stream_url: str = None

    def __init__(self, url=None, token=None, stream_url=None):
        super().__init__(url=url, token=token)
        self.set_stream_url(stream_url)

    def set_stream_url(self, stream_url):
        self.stream_url = stream_url

    def get_image(self):
        cap = cv2.VideoCapture(self.stream_url)
        while True:
            ret, frame = cap.read()
            if ret:
                return imutils.rotate(frame, self.rotation)
