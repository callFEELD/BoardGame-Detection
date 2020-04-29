# BoardGame-Detection
![CI](https://github.com/callFEELD/BoardGame-Detection/workflows/CI/badge.svg)

## Client Server Architecture
1. The client will send an image to the API server.
2. The server will response with the found pieces on the board

## Client
There are to main clients:
+ Raspberry Pi Client `PiClient`
+ `StreamClient`

### Raspberry Pi Client
The PiClient must sit on the Raspberry Pi.
It will connect to the Pi Camera with the `picamera` library.
It will take an image from the Pi Camera and sends it to the API Server.

This Raspberrry Pi Client is using `Pillow` instead of `opencv-python` to
remove the build process of OpenCV.

Make sure you installed the correct packages for Pillow on the Pi with:
```bash
sudo apt-get install python-pil
```

#### Python dependencies
+ `picamera`
+ `Pillow`
+ `numpy`
+ `aiohttp`

```python
from src.api.piclient import PiClient

client = PiClient() # this also initializes and starts the picamera
client.set_token('123456789')
client.set_url('http://127.0.0.1/analyse')

print(client.detect())
# Either none or a list with Pieces
```

### StreamClient
The StreamClient can sit anywhere. It can access a video stream of another device.
It will take the latest frame of the stream and sends it to the API Server.

#### Python dependencies
+ `opencv-python`
+ `imutils`
+ `numpy`
+ `aiohttp`

```python
from src.api.client import StreamClient

client = StreamClient()
client.set_token('123456789')
client.set_url('http://127.0.0.1/analyse')
client.set_stream_url('http://127.0.0.1:8000/image.mjpg')

print(client.detect())
# Either none or a list with Pieces
```

## Server
#### Python dependencies
+ `opencv-python`
+ `numpy`
+ `fastapi`
+ `uvicorn`
