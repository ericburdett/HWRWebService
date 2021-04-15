import time

import flask
import pymongo
from bson.json_util import dumps

import settings


def ws_create():
    ws = flask.Flask(__name__, static_url_path="", static_folder="static")
    db = pymongo.MongoClient(host=settings.MONGO_HOST, port=settings.MONGO_PORT)

    @ws.route('/', redirect_to='/index.html')
    def home():
        pass

    @ws.route(settings.WS_INFERENCES_ENDPOINT, methods=['GET'])
    def get_previous_inferences():
        results = db[settings.DB_SCHEMA][settings.DB_INFERENCES].find()
        results = list(results)

        return dumps(results), 200

    @ws.route(settings.WS_PREDICT_ENDPOINT, methods=['POST'])
    def predict():
        img = flask.request.form.get(settings.WS_PAYLOAD_IMG)

        if img:
            result = db[settings.DB_SCHEMA][settings.DB_QUEUE].insert_one(
                {settings.DB_IMG: img, settings.DB_STATUS: settings.DB_STATUS_WAITING}
            )

            object_id = result.inserted_id

            start_time = time.perf_counter()
            while time.perf_counter() - start_time < settings.TIMEOUT_TIME_S:
                output = db[settings.DB_SCHEMA][settings.DB_QUEUE].find_one_and_delete(
                    {settings.DB_ID: object_id, settings.DB_STATUS: settings.DB_STATUS_DONE}
                )

                if output:
                    # Move the result to the inferences document store
                    result = db[settings.DB_SCHEMA][settings.DB_INFERENCES].insert_one(output)
                    if result.acknowledged:
                        return '', 200
                    else:
                        return '', 500

            return '', 304

        return '', 400

    return ws


if __name__ == '__main__':
    app = ws_create()
    app.run(host=settings.WS_HOST, port=settings.WS_PORT)
