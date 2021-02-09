import base64
import numpy as np


def base64_encode_img(np_img):
    return base64.b64encode(np_img).decode('utf8')


def base64_decode_img(str_img, shape):
    img = bytes(str_img, encoding='utf8')
    img = np.frombuffer(base64.decodebytes(img), dtype="float32")
    img = img.reshape(shape)
    return img
