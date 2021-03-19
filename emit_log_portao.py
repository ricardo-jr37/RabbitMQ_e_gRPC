#!/usr/bin/env python
import pika
import sys
import time
import random

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='portao')

while True:
	#ruido = random.random() * random.randrange(-2, 2, 1)
	valor =  1
	channel.basic_publish(exchange='', routing_key='portao', body=str(valor))
	time.sleep(5)

connection.close()