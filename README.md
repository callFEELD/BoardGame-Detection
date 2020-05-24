# BoardGame-Detection
![CI](https://github.com/callFEELD/BoardGame-Detection/workflows/CI/badge.svg)
![Docker Image CI](https://github.com/callFEELD/BoardGame-Detection/workflows/Docker%20Image%20CI/badge.svg)

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
+ `numpy`
+ `pillow`
+ `aiohttp`
+ `picamera`

```python
from client.src.piclient import PiClient

# Setup the PiClient
client = PiClient(
    url='http://127.0.0.1',
    token='a_random_token_please'
)

# Ping the API server to check its uptime
#   This will return either True or False
print(client.ping())

# Send an image to detect the figures
#   This will return two variables
#       1. the list of pieces for the game logic
#       2. debug infos, if client.detect(debug=True)
pieces, _ = client.detect()
print(pieces)
```

### StreamClient
The StreamClient can sit anywhere. It can access a video stream of another device.
It will take the latest frame of the stream and sends it to the API Server.

#### Python dependencies
+ `numpy`
+ `pillow`
+ `aiohttp`
+ `opencv-python`
+ `imutils`

```python
from client.src.streamclient import StreamClient

# Setup the StreamClient
client = StreamClient(
    url='http://127.0.0.1',
    token='a_random_token_please',
    stream_url='http://127.0.0.1:8000/stream.mjpg'
)

# Ping the API server to check its uptime
#   This will return either True or False
print(client.ping())

# Send an image to detect the figures
#   This will return two variables
#       1. the list of pieces for the game logic
#       2. debug infos, if client.detect(debug=True)
pieces, _ = client.detect()
print(pieces)
```

## Server
#### Python dependencies
+ `opencv-python`
+ `numpy`
+ `fastapi`
+ `uvicorn`
