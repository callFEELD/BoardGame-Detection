from .utils import img2str

import asyncio
from PIL import Image
import numpy as np
from aiohttp import ClientSession, ClientTimeout


class Client:
    rotation: int = 90
    url: str = None
    token: str = None
    timeout: int = 30
    headers: dict = None
    image_file: str = None

    detect_debug_url: str = "/debuganalyse"
    detect_url: str = "/analyse"
    ping_url: str = "/ping"

    def __init__(self, url=None, token=None):
        self.set_server_url(url)
        self.set_token(token)

    def set_image_file(self, image_file):
        self.image_file = image_file

    def ping(self):
        """
        Pings the server
            returns:
                True -- if server is up
                False -- if server is down
        """
        try:
            loop = asyncio.get_event_loop()
            ret = loop.run_until_complete(
                self._request(
                    self.url + self.ping_url,
                    req_type="get"
                )
            )
            if ret == {}:
                return True
            else:
                return False
        except Exception:
            return False

    def get_image(self):
        """
        This function will get the image which will be send
        via the request command.

        This function will be overriden for the individual clients.

        returns:
            np.array as the image
        """
        image = Image.open(self.image_file)
        image = image.rotate(self.rotation)
        image = np.array(image)
        # Convert RGB to BGR
        return image[:, :, ::-1].copy()

    def set_token(self, token: str):
        """
        Sets the API token to access the api server.

        This token will be send for each request to verify
        that the client is allowed to make requests.
        """
        self.token = token
        self.headers = {
            'X-authentication-token': self.token
        }

    def set_server_url(self, url: str):
        """
        Sets the api server url.
        !Important Make sure you the url does NOT end with a /
        """
        self.url = url

    async def _request(self, url, json={}, req_type="post"):
        timeout = ClientTimeout(total=self.timeout)

        async with ClientSession(timeout=timeout) as session:
            # make a valid move
            if req_type == "post":
                async with session.post(url, headers=self.headers,
                                        json=json) as resp:
                    assert resp.status == 200
                    return await resp.json()
            elif req_type == "get":
                async with session.get(url, headers=self.headers) as resp:
                    assert resp.status == 200
                    return await resp.json()

    def detect(self, options=None, debug=False):
        """
        Sends the image via an api request to the server
        and waits for the answer.

        returns:
            1. list of pieces or None
            2. debug information or None
        """
        # get the current image
        image = self.get_image()

        json = {
            "image": img2str(image),
            "options": options
        }

        loop = asyncio.get_event_loop()
        if debug:
            ret = loop.run_until_complete(
                self._request(
                    self.url + self.detect_debug_url,
                    json
                )
            )
            return ret["pieces"], ret["debug"]
        else:
            ret = loop.run_until_complete(
                self._request(
                    self.url + self.detect_url,
                    json
                )
            )
            return ret, None
