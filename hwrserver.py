import time

import tensorflow as tf
import pymongo

from hwr import models, dataset
from hwr.util import bp_decode

import settings


CHARS = " !\"#%&'()*+,-./0123456789:;<=>?ABCDEFGHIJKLMNOPQRSTUVWXYZ[]_abcdefghijklmnopqrstuvwxyz{|}£¤§°²ÀÉàâçèéêëîôùûœſ€⊥𐌰𐌳𐌴𐌵𐌸𐌺𐌻𐌼𐌾𐍆𐍈"


def main():
    model = models.FlorRecognizer(vocabulary_size=len(CHARS) + 1)
    model.load_weights(settings.HWR_WEIGHTS_PATH)

    idx2char = dataset.get_idx2char(CHARS)

    db = pymongo.MongoClient(host=settings.MONGO_HOST, port=settings.MONGO_PORT)

    # Continually check the Mongo queue to see if there are more images to perform classification
    while True:
        instance = db[settings.DB_SCHEMA][settings.DB_QUEUE].find_one_and_update(
            {settings.DB_STATUS: settings.DB_STATUS_WAITING},
            {'$set': {settings.DB_STATUS: settings.DB_STATUS_PROCESSING}},
            fields={settings.DB_ID: 1, settings.DB_IMG: 1}
        )

        # If there is an instance to pull off the queue that requires inference
        if instance is not None:
            id = instance[settings.DB_ID]
            img = instance[settings.DB_IMG][22:]

            img = tf.io.decode_base64(img)
            img = tf.image.decode_image(img, channels=1)

            # Convert to tensor and expand batch dimension
            img = dataset.img_resize_with_pad(img, settings.IMG_SIZE)
            img = tf.expand_dims(img, 0)
            img = tf.image.per_image_standardization(img)

            output = model(img)
            predictions = bp_decode(output)

            predictions = tf.squeeze(predictions, 0)
            str_prediction = dataset.idxs_to_str(predictions, idx2char, merge_repeated=True).numpy().decode('utf8')

            result = db[settings.DB_SCHEMA][settings.DB_QUEUE].update_one(
                {settings.DB_ID: id},
                {'$set': {settings.DB_STATUS: settings.DB_STATUS_DONE, settings.DB_TRANSCRIPTION: str_prediction}}
            )

            if result.acknowledged:
                print('Performed Inference: ', str_prediction)
            else:
                print('Error occurred while adding transcription to Mongo')

        # If there are no images to pull off the queue for inference
        else:
            print('No images in the Queue...')
            time.sleep(settings.MODEL_SLEEP_S)


if __name__ == '__main__':
    main()
