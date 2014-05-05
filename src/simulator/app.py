import pika, os, urlparse, random, pytz
from time import sleep
from datetime import datetime

queueName = "task_queue"
url_str = os.environ.get('CLOUDAMQP_URL', '')
url = urlparse.urlparse(url_str)

params = pika.ConnectionParameters(
	host=url.hostname, 
	virtual_host=url.path[1:],
    credentials=pika.PlainCredentials(url.username, url.password))

connection = pika.BlockingConnection(params)

# Open the channel
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue=queueName,
					  durable=True,
					  exclusive=False,
					  auto_delete=False)

try:

	while True:

		# Create test data
		c_r = random.uniform(-1, 1)
		f_r = random.uniform(-5, 5)
		c = 25.875 + c_r
		f = 78.575 + f_r
		now = datetime.now(pytz.utc)

		message = "{0},{1},{2}".format(c, f, now)
		
		# Send a message
		channel.basic_publish(exchange='', 
							  routing_key=queueName, 
							  body=message,
							  properties=pika.BasicProperties(
		                         delivery_mode = 2, # make message persistent
		                      ),
							  mandatory=True)

		print " [x] Sent: %s" % message

		sleep(5)

except KeyboardInterrupt:

	connection.close()