import os
import requests
from threading import Thread, Lock
import time
import itertools

import settings

IMG_DIR = './data/images'
REQUESTS_PER_IMAGE = 1000


class AtomicInt(object):
    def __init__(self, start=0, step=1):
        self.num_reads = 0
        self.counter = itertools.count(start=start, step=step)
        self.read_lock = Lock()

    def increment(self):
        next(self.counter)

    def value(self):
        with self.read_lock:
            value = next(self.counter) - self.num_reads
            self.num_reads += 1
        return value


success_counter = AtomicInt()
failure_counter = AtomicInt()


def inference(img_path, thread_id):
    img = open(img_path, 'rb').read()
    payload = {settings.WS_PAYLOAD_IMG: img}

    print('Submitting ', thread_id)
    r = requests.post('http://' + settings.WS_HOST + ':' + str(settings.WS_PORT) + settings.WS_PREDICT_ENDPOINT, files=payload).json()

    if r[settings.WS_PAYLOAD_SUCCESS]:
        success_counter.increment()
        print('Thread: {}, Status: {}, Prediction: {}'.format(
            thread_id, 'Success', r[settings.WS_PAYLOAD_PREDICTION]))
    else:
        failure_counter.increment()
        print('Thread: {}, Status: {}'.format(thread_id, 'Failed'))


def main():
    img_paths = os.listdir(IMG_DIR)

    threads = []
    for img_path in img_paths:
        for i in range(REQUESTS_PER_IMAGE):
            t = Thread(target=inference, args=(os.path.join(IMG_DIR, img_path), img_path + '_' + str(i)))
            t.daemon = True
            t.start()
            threads.append(t)
            time.sleep(settings.TEST_REQUEST_SLEEP_S)

    for t in threads:
        t.join()

    print('Successful Inferences:', success_counter.value())
    print('Failed Inferences:', failure_counter.value())


if __name__ == '__main__':
    main()
