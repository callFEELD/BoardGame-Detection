import asyncio
import cv2
import base64
import pickle


from aiohttp import ClientSession, ClientTimeout


def img2str(image):
    imdata = pickle.dumps(image)
    return base64.b64encode(imdata).decode('ascii')


headers: dict = {
    'X-authentication-token': '123456789'
}

img = cv2.imread("data/checkers2.jpg")

test: dict = {
    "image": img2str(img),
    "options": None
}


async def make_requests():
    timeout = ClientTimeout(total=(60 * 9))

    async with ClientSession(timeout=timeout) as session:
        # make a valid move
        async with session.post("http://127.0.0.1:8000/analyse", headers=headers, json=test) as resp:
            j = await resp.json()
            assert isinstance(j, dict)
            assert resp.status == 200


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(make_requests())