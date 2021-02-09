import time
import json

import tensorflow as tf
import numpy as np
import redis
from hwr import models, dataset
from hwr.util import bp_decode
import matplotlib.pyplot as plt


import settings
import helpers


CHARS = " !\"#%&'()*+,-./0123456789:;<=>?ABCDEFGHIJKLMNOPQRSTUVWXYZ[]_abcdefghijklmnopqrstuvwxyz{|}£¤§°²ÀÉàâçèéêëîôùûœſ€⊥𐌰𐌳𐌴𐌵𐌸𐌺𐌻𐌼𐌾𐍆𐍈"


def main():
    model = models.FlorRecognizer(vocabulary_size=len(CHARS) + 1)
    model.load_weights(settings.HWR_WEIGHTS_PATH)

    idx2char = dataset.get_idx2char(CHARS)

    db = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

    # Continually check the Redis queue to see if there are more images to perform classification
    while True:
        queue = db.lrange(settings.QUEUE_NAME, 0, settings.BATCH_SIZE - 1)

        if not queue:
            print('No images in the Queue...')
            time.sleep(settings.MODEL_SLEEP_S)
            continue

        batch = None

        ids = []
        for q in queue:
            q = json.loads(q.decode('utf8'))
            img = helpers.base64_decode_img(q[settings.WS_PAYLOAD_IMG], settings.IMG_SIZE)

            # Convert to tensor and expand batch dimension
            img = tf.constant(img)
            img = tf.expand_dims(img, 2)
            img = tf.expand_dims(img, 0)
            img = tf.image.per_image_standardization(img)

            if batch is None:
                batch = img
            else:
                batch = tf.concat((batch, img), axis=0)

            ids.append(q[settings.WS_PAYLOAD_ID])

        output = model(batch)
        predictions = bp_decode(output)
        str_predictions = dataset.idxs_to_str_batch(predictions, idx2char, merge_repeated=True).numpy()

        for str_prediction, id in zip(str_predictions, ids):
            decoded_prediction = str_prediction.decode('utf8')
            print('Prediction:', decoded_prediction)

            db.set(id, decoded_prediction)

        db.ltrim(settings.QUEUE_NAME, len(queue), -1)


if __name__ == '__main__':
    main()
