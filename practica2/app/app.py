from flask import Flask
from app.ejP1 import adivinaElNumero as ej1p1
from app.ejP1 import ordenacionMatrices as ej2p1
from app.ejP1 import cribaEratostenes as ej3p1
from app.ejP1 import fibonacciFichero as ej4p1
from app.ejP1 import cadenasCorchetes as ej5p1
from app.ejP1 import expresionesRegulares as ej6p1

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/ejercicio2/<string:matriz>')
def ejercicio2(matriz):
    return list(matriz)
