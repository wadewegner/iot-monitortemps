import os, psycopg2, urlparse, pika

queueName = "message"

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

cur = conn.cursor()

url_str = os.environ.get('CLOUDAMQP_URL', '')
url = urlparse.urlparse(url_str)

params = pika.ConnectionParameters(
	host=url.hostname,
	virtual_host=url.path[1:],
    credentials=pika.PlainCredentials(url.username, url.password))

connection = pika.BlockingConnection(params)
channel = connection.channel()

def callback(ch, method, properties, body):

	records = [x.strip() for x in body.split(',')]

	cur.execute('INSERT INTO iot_monitortemps.readings__c (celsius__c, fahrenheit__c, readingdatetime__c) ' +
		'VALUES (%s, %s, %s)', 
		(records[0],records[1],records[2]))

	conn.commit()

	print " [x] Inserted: %s" % str(records)

	ch.basic_ack(delivery_tag=method.delivery_tag)

try:

	channel.basic_consume(callback,
	    queue=queueName,
	    no_ack=False)

	channel.start_consuming()

except KeyboardInterrupt:
	
	channel.stop_consuming()
	cur.close()
	conn.close()

connection.close()