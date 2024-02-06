import json
import random

from .queue.event_producer import EventProducer

class MachineLearning(object):
    def __init__(self):
        pass

    def generate_random_coordinates(self):
        top_left_x = random.randint(0, 800)
        top_left_y = random.randint(0, 600)
        width = random.randint(50, 200)
        height = random.randint(50, 200)
        confidence = round(random.uniform(0.7, 1.0), 2)

        return [top_left_x, top_left_y, width, height, confidence,
                1]  # 1 - класс для автомобиля

    def call(self, data):
        data_dict = json.loads(data)

        if random.choice([True, False]):
            data_dict['payload'] = []
            return json.dumps(data_dict)
        else:
            data_dict['payload'] = self.generate_random_coordinates()
            return json.dumps(data_dict)
