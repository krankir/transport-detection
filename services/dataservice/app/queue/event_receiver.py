import json

import pika
from app.machine_learning import MachineLearning


class EventReceiver(object):
    def __init__(self):
        credentials = pika.PlainCredentials('skipper', 'welcome1')
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq',
                                                                       port=5672,
                                                                       credentials=credentials))

        channel = connection.channel()
        channel.queue_declare(queue='machine_learning')

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue='machine_learning', on_message_callback=self.on_request)

        print("Awaiting requests for [x] data service [x]")
        channel.start_consuming()

    def on_request(self, ch, method, props, body):
        print(f'{ch=}, {method=}, {props=}, {body=}')
        machine_learning = MachineLearning()
        response_ = machine_learning.call(body)
        response = json.dumps(response_)

        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id=props.correlation_id),
                         body=response)
        ch.basic_ack(delivery_tag=method.delivery_tag)

        print('Processed response:', response)
