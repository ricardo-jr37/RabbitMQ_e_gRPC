import time
from flask import Flask, url_for, jsonify
from flask import render_template
from flask import request
import socket
import pdb
import pickle
import time
import json
PORT = 5000
HOST = 'localhost'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def create():
    result = json.dumps(request.form)
    print(result)
    #ligada = request.form.get('lampada')
    #ar = request.form.get('ar')
    s.send(result.encode('utf-8'))
    
    return render_template('index.html')
    '''
    if int(ar) == 1:
        print(request.form.get('temperatura'))
    else:
        print('ar-desligado')
    if int(ligada) == 1:
        palavra = 'teste_conexao'
        print(ligada)
        PORT = 5000
        HOST = 'localhost'
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.send(palavra.encode('utf-8'))
    else:
        palavra = 'teste_conexao_desligada'
        print(ligada)
        PORT = 5000
        HOST = 'localhost'
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.send(palavra.encode('utf-8'))    
    return render_template('index.html')
    #time.sleep(5)
    '''
'''
def server_lampada(ligada):
    teste = Sensor()
    teste.nome = 'lampada'
    teste.status_lampada = int(ligada)
    PORT = 1510
    HOST = 'localhost'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall(teste.SerializeToString())
'''

if __name__ == '__main__':
    app.run(port=8080, debug=True)