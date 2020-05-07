from src.api.client import StreamClient
from src.api.utils import str2img
import cv2


client = StreamClient()
client.set_token('123456789')
client.set_url('http://127.0.0.1/debuganalyse')
client.set_stream_url('http://192.168.255.10:8000/stream.mjpg')

result = client.detect()
print(result["pieces"])

for layer in result["debug"]:
    if layer["name"] == "Debug Function: board perspective":
        cv2.imwrite("board_perspective.png", str2img(layer["img"]))
    cv2.imshow(layer["name"], str2img(layer["img"]))

cv2.waitKey(0)
cv2.destroyAllWindows()
