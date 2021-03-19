#!/usr/bin/env python
#!/usr/bin/python 
import socket
import threading
import grpc
from concurrent import futures
import pika, sys, os, time
# import the generated classes
import lampada_pb2
import lampada_pb2_grpc
# import the generated classes
import ar_pb2
import ar_pb2_grpc
# import the generated classes
import portao_pb2
import portao_pb2_grpc
import json
#Conexao socket
IP = "127.0.0.1"
PORT = 5000
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((str(IP), int(PORT)))
sock.listen(10)
sock.setblocking(False)
clientes = []

#Inicializando os sensores
# Lampada
sensor_ilumicao = []
sensor_ilumicao.append(0)
lampada_valor = []
lampada_valor.append(0)
# Ar
ar_sensor = []
ar_sensor.append(0)
ar_valor = []
ar_valor.append(0)

#Portão
portao_sensor = []
portao_sensor.append(0)
portao_valor = []
portao_valor.append(0)

def aceptarCon():
	print("aceptarCon iniciado")
	global sensor_ilumicao
	global lampada_valor
	global clientes
	global sock
	while True:
		try:
			stauts_portao = ""
			conn, addr = sock.accept()
			conn.setblocking(False)
			clientes.append(conn)
			#print(conn.getpeername()[1])
			valorluminosidade = int(lampada_valor[len(lampada_valor)-1]) - int(sensor_ilumicao[len(sensor_ilumicao)-1])
			#valortemperatura = 0
			#print(ar_sensor)
			if int(ar_valor[len(ar_valor)-1]) >= 0 and len(ar_valor)>1:
				valortemperatura = int(ar_valor[len(ar_valor)-1])
			else:
				valortemperatura = ar_sensor[len(ar_sensor)-1]
			if valorluminosidade < 0:
				valorluminosidade *= -1
			
			#print(len(portao_valor))
			
			if len(portao_valor)>1:
				if portao_valor[len(portao_valor)-1] >= 1:
					stauts_portao = "Aberto"
				else:
					stauts_portao = "Fechado"
			else:
				if portao_sensor[len(portao_sensor)-1] >= 1:
					stauts_portao = "Aberto"
				else:
					stauts_portao = "Fechado"
			#print(stauts_portao)
			conn.send(('HTTP/1.0 200 OK\n').encode('utf-8'))
			conn.send(('Content-Type: text/html\n').encode('utf-8'))
			conn.send(('\n').encode('utf-8')) # header and body should be separated by additional newline
			conn.send(("""
			    <html>
			    <meta charset="utf-8"/>
			        <body>
			            <h1>Trabalho 3 - SISTEMAS DISTRIBUÍDOS</h1>
			            <h3>Nivel de luminosidade (Candela): {}</h3>
			            <h3>Temperatura (C°): {}</h3>
			            <h3>Portão: {}</h3>
			            <br><a href="http://localhost:8080/">Modificar Estado</a>
			        </body>
			    </html>
			""").format(valorluminosidade, valortemperatura, stauts_portao).encode('utf-8'))
			#time.sleep(3)
		except:
			pass


def procesarCon():
	print("ProcesarCon iniciado")
	global clientes
	while True:
		if len(clientes) > 0:
			for c in clientes:
				try:
					data = c.recv(1024)
					teste = data.decode('utf-8')
					if data:

						y = json.loads(teste)
						print(y)
						procform(y)
						
				except:
					pass

def procform(y):
	if int(y['lampada']) == 1:
		comando = 'ligar'
		lampada(comando)
	else:
		comando = 'desligar'
		lampada(comando)
	if int(y['ar']) == 1:
		ar(float(y['temperatura']))
	else:
		ar(0)
	if int(y['portao']) > 0:
		portao(int(y['portao']))
	else:
		portao(int(y['portao']))

def sub_lampada():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='lampada')

    def callback(ch, method, properties, body):
        valor = int(float(body.decode()))
        global sensor_ilumicao 
        sensor_ilumicao.append(valor)


    channel.basic_consume(queue='lampada', on_message_callback=callback, auto_ack=True)

    channel.start_consuming()

def sub_ar():
	connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()
	channel.queue_declare(queue='ar')
	def callback(ch, method, properties, body):
		valor = int(float(body.decode()))
		global ar_sensor
		ar_sensor.append(valor) 


	channel.basic_consume(queue='ar', on_message_callback=callback, auto_ack=True)
    

	channel.start_consuming()

def sub_portao():

	connection = pika.BlockingConnection(
		pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()
	channel.queue_declare(queue='portao')
	def callback(ch, method, properties, body):
		valor = body.decode()

		global portao_sensor
		portao_sensor.append(int(valor))

	
	channel.basic_consume(queue='portao', on_message_callback=callback, auto_ack=True)
    

	channel.start_consuming()

def portao(comando):
	
	channel = grpc.insecure_channel('localhost:50053')
	stub = portao_pb2_grpc.PortaoStub(channel)
	# create a valid request message
	if float(comando)>=0:
		status = portao_pb2.StatusPortao(status=float(comando))
		# make the call
		response = stub.abrirPortao(status)
	else:
		status = portao_pb2.StatusPortao(status=float(comando))
		# make the call
		response = stub.fecharPortao(status)


	portao_valor.append(response.status)


def ar(comando):
	channel = grpc.insecure_channel('localhost:50052')
	stub = ar_pb2_grpc.ArStub(channel)

	if float(comando)>0:
		status = ar_pb2.ArTemperatura(temperatura=float(comando))
		# make the call
		response = stub.ligarAr(status)
	else:
		status = ar_pb2.ArTemperatura(temperatura=-1)
		# make the call
		response = stub.desligarAr(status)

	ar_valor.append(response.temperatura)
	#print(ar_valor)

def lampada(comando):
	# open a gRPC channel
	channel = grpc.insecure_channel('localhost:50051')
	# create a stub (client)
	stub = lampada_pb2_grpc.LampadaStub(channel)
	# create a valid request message
	status = lampada_pb2.LampadaStatus(stauts=1)
	# make the call
	
	if comando == 'desligar':
		response = stub.desligarLampada(status)
	else:
		response = stub.ligarLampada(status)

	lampada_valor.append(response.stauts)
	



t = threading.Thread(target=sub_lampada)
t.start()

#t2 = threading.Thread(target=sensores)
#t2.start()

t3 = threading.Thread(target=sub_ar)
t3.start()
#sub_portao

t4=threading.Thread(target=sub_portao)
t4.start()

aceptar = threading.Thread(target=aceptarCon)
aceptar.start()

procesar = threading.Thread(target=procesarCon)
procesar.start()

while True:
	try:
		
		
		comando = input('')
	
	except KeyboardInterrupt:
		print('Interrupted')
		try:
			sys.exit(0)
			sock.close()
		except SystemExit:
			sock.close()
			os._exit(0)

