# Redis Server Information
MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27018

# Web Server Information
WS_HOST = '127.0.0.1'
WS_PORT = 5000
WS_PREDICT_ENDPOINT = '/predict'
WS_INFERENCES_ENDPOINT = '/inferences'

# Names for the request, response keys
WS_PAYLOAD_ID = 'id'
WS_PAYLOAD_IMG = 'img'
WS_PAYLOAD_SUCCESS = 'success'
WS_PAYLOAD_PREDICTION = 'prediction'

DB_SCHEMA = 'journal'
DB_QUEUE = 'queue'
DB_INFERENCES = 'inferences'

DB_ID = "_id"
DB_STATUS = "status"
DB_IMG = "img"
DB_TRANSCRIPTION = "transcription"

DB_STATUS_WAITING = "WAITING"
DB_STATUS_PROCESSING = "PROCESSING"
DB_STATUS_DONE = "DONE"

# Model Configuration Settings
IMG_SIZE = (64, 1024)  # Height and Width for the resized image
BATCH_SIZE = 128  # The batch size used for inference on the model
HWR_WEIGHTS_PATH = './data/model_weights/iam_hwr_line_level_model/run1' # Path to the pre-trained model
TEST_IMG_DIR = './data/images'  # The directory used for test images

# Sleep/Timeout times in seconds
TIMEOUT_TIME_S = 15  # How long do we wait for model inference until returning a failure response
CLIENT_SLEEP_S = 1  # How long do we sleep in between checking to see if the model has performed inference on an image
MODEL_SLEEP_S = 1  # How long does the model sleep in between checking to see if new images have been added to the queue
TEST_REQUEST_SLEEP_S = .05  # Time inbetween subsequent requests

# Named of Redis Queue
QUEUE_NAME = 'image_queue'



