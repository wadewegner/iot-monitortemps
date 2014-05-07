import pika, os, urlparse, random, pytz, glob
from time import sleep
from datetime import datetime

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():

    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

def pub_message(temp_c, temp_f, sensorId):

	now = datetime.now(pytz.utc)
	message = "{0},{1},{2},{3}".format(temp_c, temp_f, sensorId, now)
	
	# Send a message
	channel.basic_publish(exchange='', 
						  routing_key=queueName, 
						  body=message,
						  properties=pika.BasicProperties(
	                         delivery_mode = 2, # make message persistent
	                      ),
						  mandatory=True)

	print " [x] Sent: %s" % message

# Variables
queueName = "task_queue"
url_str = os.environ.get('CLOUDAMQP_URL', '')
url = urlparse.urlparse(url_str)

# Set GPIO details
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'

# Setup connection
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
	print "Running"

	while True:

		temp_c = 0;
		temp_f = 0;
		
		sensorId = "28-00000557d264"
		device_file = base_dir + sensorId + '/w1_slave'

		temp_c, temp_f = read_temp()
		pub_message(temp_c, temp_f, sensorId)

		sensorId = "28-000005584db5"
		device_file = base_dir + sensorId + '/w1_slave'

		temp_c, temp_f = read_temp()
		pub_message(temp_c, temp_f, sensorId)

		sleep(1)

except KeyboardInterrupt:

	connection.close()