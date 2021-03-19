#!/usr/bin/env python
import pika
import sys
import time
import random

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='lampada')

while True:
	ruido = random.random() * random.randrange(-5, 5, 1)
	valor =  15 + ruido
	channel.basic_publish(exchange='', routing_key='lampada', body=str(valor))
	time.sleep(5)

connection.close()