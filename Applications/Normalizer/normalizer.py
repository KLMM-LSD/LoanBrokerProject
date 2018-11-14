# Author:......KRG
# Description:.Normalizer to receive loan quotes in different formats and send them on as JSON.
from collections import defaultdict
import pika, json, lxml, requests
	
def getCorrelationID(header_frame):
	return

def jsonQuote(channel, method_frame, header_frame, body):        
	dict = json.loads(body)

	toAggregator(dict)
	return

def xmlQuote(channel, method_frame, header_frame, body):
	
	dict = {}
	
	toAggregator(dict)
	return

def toAggregator(dictionary):
	dictionary['bankID'] = getCorrelationID(header_frame)
	
	request = requests.post('localhost:8081/postQuote', data=json.dumps(dictionary))
	return
	
def start():
	conn = pika.BlockingConnection()
	channel = conn.channel()
	xmlQueue = channel.declare('klmm.normalize.xml', passive=True, durable=True ...)
	jsonQueue = channel.declare('klmm.normalize.json', passive=True, durable=True ...)
	
	channel.basic_consume(xmlQuote, xmlQueue, no-ack=True)
	channel.basic_consume(jsonQuote, jsonQueue, no-ack=True)
	
	#Ensuring that default sigint handler is ready
	signal.signal(signal.SIGINT, signal.default_int_handler)
	try:
		channel.start_consuming()
	except KeyboardInterrupt:
		conn.close(reply_code=200, reply_text='Normal shutdown)

start()

