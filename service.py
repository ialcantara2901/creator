# service.py

import pika
import json

class RabbitMQService:
    def __init__(self):
        self.credentials = pika.PlainCredentials("admin", "Fa230130")
        self.parameters = pika.ConnectionParameters('rabbitmq', 5672, 'default', self.credentials)
    
    def connect(self):
        connection = pika.BlockingConnection(self.parameters)
        return connection

    def declare_queue(self, channel, queue_name):
        channel.queue_declare(queue=queue_name)

    def consume_messages(self, queue_name, callback):
        connection = self.connect()
        channel = connection.channel()
        self.declare_queue(channel, queue_name)

        def on_message(ch, method, properties, body):
            message = json.loads(body)
            callback(message)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        channel.basic_consume(queue=queue_name, on_message_callback=on_message)
        print(f'[*] Waiting for messages in {queue_name}. To exit press CTRL+C')
        channel.start_consuming()

    def send_message(self, queue_name, message):
        connection = self.connect()
        channel = connection.channel()
        self.declare_queue(channel, queue_name)
        channel.basic_publish(exchange='', routing_key=queue_name, body=json.dumps(message))
        connection.close()
