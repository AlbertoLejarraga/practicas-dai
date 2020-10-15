from flask import Flask
from app.ejp1.adivinaElNumero import *
from app.ejp1.ordenacionMatrices import *
from app.ejp1.cribaEratostenes import *
from app.ejp1.fibonacciFichero import *
from app.ejp1.cadenasCorchetes import *
from app.ejp1.expresionesRegulares import *
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/ejercicio2/<string:matriz>')
def ejercicio2(matriz):
    return list(matriz)
