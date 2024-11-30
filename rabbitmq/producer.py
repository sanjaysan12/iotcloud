import pika
import random
import time

# Uses AMQP to communicate

credentials = pika.PlainCredentials('Sanjay', 'Sanjay12')
parameters = pika.ConnectionParameters('rabbitmq.selfmade.ninja',
                                       5672,
                                       'ksanjay02444_test',
                                       credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue='my_first_queue')

# while True:
message = "Hi Iam Sanjay"
channel.basic_publish(exchange='',
                        routing_key='my_first_queue',
                        body=message)
print(" [x] Sent '{}!'".format(message))
    # time.sleep(0.001)

connection.close()