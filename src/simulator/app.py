import pika, os, urlparse, random, pytz
from time import sleep
from datetime import datetime

queueName = "message"
url_str = os.environ.get('CLOUDAMQP_URL', '')
url = urlparse.urlparse(url_str)

params = pika.ConnectionParameters(
	host=url.hostname, 
	virtual_host=url.path[1:],
    credentials=pika.PlainCredentials(url.username, url.password))

connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue=queueName)

try:

	while True:

		c_r = random.uniform(-1, 1)
		f_r = random.uniform(-5, 5)
		c = 25.875 + c_r
		f = 78.575 + f_r
		now = datetime.now(pytz.utc)

		message = "{0},{1},{2}".format(c, f, now)
		channel.basic_publish(exchange='', routing_key=queueName, body=message)

		print " [x] Sent: %s" % message

		sleep(.5)

except KeyboardInterrupt:

	connection.close()