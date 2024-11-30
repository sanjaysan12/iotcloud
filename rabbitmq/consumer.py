import pika

# Uses AMQP to communicate
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

credentials = pika.PlainCredentials('Sanjay', 'Sanjay12')
parameters = pika.ConnectionParameters('rabbitmq.selfmade.ninja',
                                       5672,
                                       'ksanjay02444_test',
                                       credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()


channel.queue_declare(queue='my_first_queue')

channel.basic_consume(queue='my_first_queue',
                      auto_ack=True,
                      on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()