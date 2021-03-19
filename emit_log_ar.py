#!/usr/bin/env python
import pika
import sys
import time
import random

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='ar')

while True:
	ruido = random.random() * random.randrange(-2, 2, 1)
	valor =  30 + ruido
	channel.basic_publish(exchange='', routing_key='ar', body=str(valor))
	time.sleep(5)

connection.close()