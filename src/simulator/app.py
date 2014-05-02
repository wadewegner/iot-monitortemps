import pika, os, urlparse, logging
from time import sleep
import random

logging.basicConfig()

cloudAMQP_URL = 'amqp://tlojvxhf:_xaDrzsuDcsF5aVbzaUO9y18lVl-X7aW@turtle.rmq.cloudamqp.com/tlojvxhf'
queueName = "message"

url_str = os.environ.get('CLOUDAMQP_URL', cloudAMQP_URL)
url = urlparse.urlparse(url_str)
params = pika.ConnectionParameters(host=url.hostname, virtual_host=url.path[1:],
    credentials=pika.PlainCredentials(url.username, url.password))

connection = pika.BlockingConnection(params) # connect to CloudAMQP
channel = connection.channel() # start a channel
channel.queue_declare(queue=queueName) # declare a queue

while True:

	# send a message
	c_r = random.uniform(-1, 1)
	f_r = random.uniform(-5, 5)

	c = 25.875 + c_r
	f = 78.575 + f_r
	message = "({0}, {1})".format(c, f)
	channel.basic_publish(exchange='', routing_key=queueName, body=message)
	print " [x] Sent: %s" % message

	sleep(0.5)






# # create a function which is called on incoming messages
# def callback(ch, method, properties, body):
#   print " [x] Received %r" % (body)

# # set up subscription on the queue
# channel.basic_consume(callback,
#     queue=queueName,
#     no_ack=True)

# channel.start_consuming() # start consuming (blocks)

# connection.close()