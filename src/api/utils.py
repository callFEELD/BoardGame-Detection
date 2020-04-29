import numpy as np
import base64
import pickle


def img2str(image):
    imdata = pickle.dumps(image)
    return base64.b64encode(imdata).decode('ascii')


def str2img(string):
    image = base64.b64decode(string)
    image = pickle.loads(image)
    return np.array(image)
