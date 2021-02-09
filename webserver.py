import uuid
import json
import time
import io
import base64

import flask
import redis
import numpy as np
from PIL import Image
from hwr.dataset import img_resize_with_pad

import settings
import helpers


def preprocess(img):
    if len(img.shape) == 2:
        img = np.expand_dims(img, 2)
    img = img_resize_with_pad(img, settings.IMG_SIZE)
    img = img.numpy()
    img.copy(order='C')

    return img


def ws_create():
    ws = flask.Flask(__name__)
    db = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
    db.delete(settings.QUEUE_NAME)

    @ws.route('/')
    def home():
        return "Python Flask Web Server"

    @ws.route(settings.WS_PREDICT_ENDPOINT, methods=['POST'])
    def predict():
        data = {settings.WS_PAYLOAD_SUCCESS: False}

        if flask.request.files.get(settings.WS_PAYLOAD_IMG):
            img = flask.request.files[settings.WS_PAYLOAD_IMG].read()
            img = np.array(Image.open(io.BytesIO(img)))
            img = preprocess(img)
            img = helpers.base64_encode_img(img)

            unique_id = str(uuid.uuid4())

            payload = {settings.WS_PAYLOAD_ID: unique_id, settings.WS_PAYLOAD_IMG: img}
            db.rpush(settings.QUEUE_NAME, json.dumps(payload))

            # Loop until we have a prediction
            start_time = time.perf_counter()
            while time.perf_counter() - start_time < settings.TIMEOUT_TIME_S:
                output = db.get(unique_id)

                if output is not None:
                    output = output.decode('utf8')
                    data[settings.WS_PAYLOAD_SUCCESS] = True
                    data[settings.WS_PAYLOAD_PREDICTION] = output

                    # Delete id from Redis
                    db.delete(unique_id)

                    # break from loop
                    break

                else:
                    time.sleep(settings.CLIENT_SLEEP_S)

        return flask.jsonify(data)

    return ws


if __name__ == '__main__':
    app = ws_create()
    app.run(host=settings.WS_HOST, port=settings.WS_PORT)
