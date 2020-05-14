from client.src.streamclient import StreamClient
from client.src.utils import str2img
import cv2


client = StreamClient(
    url='http://127.0.0.1',
    token='a_random_token_please',
    stream_url='http://192.168.255.10:8000/stream.mjpg'
)

print(client.ping())

result, debug = client.detect(debug=True)
print(result)

for layer in debug:
    if layer["name"] == "Debug Function: board perspective":
        cv2.imwrite("board_perspective.png", str2img(layer["img"]))
    cv2.imshow(layer["name"], str2img(layer["img"]))


if result is not None:
    for i in range(32):
        inside = False
        for piece in result:
            if i+1 == piece["position"]:
                if piece["player"] == 1 and piece["king"]:
                    print("W", end="")
                    inside = True
                elif piece["player"] == 1 and not piece["king"]:
                    print("w", end="")
                    inside = True
                elif piece["player"] == 2 and piece["king"]:
                    print("B", end="")
                    inside = True
                else:
                    print("b", end="")
                    inside = True
        if not inside:
            print("0", end='')
        else:
            inside = False

cv2.waitKey(0)
cv2.destroyAllWindows()
