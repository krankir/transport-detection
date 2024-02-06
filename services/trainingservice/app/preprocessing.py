import base64
import json
import cv2

import numpy as np

from .queue.event_producer import EventProducer


class Preprocessing(object):
    def __init__(self):
        pass

    def call(self, body):
        data_dict = json.loads(body)
        data_img = data_dict['payload']
        decoded_bytes_img = base64.b64decode(data_img)
        numpy_array_img = np.frombuffer(decoded_bytes_img, dtype=np.uint8)
        image = cv2.imdecode(numpy_array_img, flags=cv2.IMREAD_UNCHANGED)
        desired_size = (640, 640)
        resized_image = cv2.resize(image, desired_size)
        normalized_image = cv2.normalize(resized_image, None, 0.0, 1.0,
                                         cv2.NORM_MINMAX)
        image_bytes = cv2.imencode('.png', normalized_image)[1].tobytes()
        base64_string = base64.b64encode(image_bytes).decode('utf-8')

        data_dict['payload'] = base64_string

        if data_dict['steps']:
            next_steps_queue = data_dict['steps'].pop(0)
            data = json.dumps(data_dict)
            data_dict = self.prepare_datasets(next_steps_queue, data)

        return data_dict

    def prepare_datasets(self, next_steps_queue, data_dict):
        event_producer = EventProducer()
        response = event_producer.call(next_steps_queue, data_dict)
        return response
