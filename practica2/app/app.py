from flask import Flask
from app.ejp1.adivinaElNumero import *
from app.ejp1.ordenacionMatrices import ordenarMatrices
from app.ejp1.cribaEratostenes import *
from app.ejp1.fibonacciFichero import *
from app.ejp1.cadenasCorchetes import *
from app.ejp1.expresionesRegulares import *
import random

app = Flask(__name__)
def generarCabeceras(titulo):
    return "<html>" \
             "<head>" \
             "<title>" + titulo + "</title>" \
             "</head>" \
             "<body>"
@app.route('/')
def hello_world():
    salida = generarCabeceras("Inicio")
    salida = "<h1>Página principal para la práctica 2 de DAI 2020</h1>" \
             "<ul>" \
                "<li><a href='ejercicio2/1,6,7,9,4,3,2,8,5,1'>Ejercicio 2: Ordenación de matrices</a>" \
             "</ul></body></html>"
    return salida

@app.route('/ejercicio2/<string:matriz>')
def ejercicio2(matriz):
    salida = generarCabeceras("Ejercicio 2")
    salida += "<span>La matriz recibida es: \n[" + matriz + "]\n</span>"
    #Se comprueba que el formato de la matriz sea correcto, se divide por comas y cada elemento es un entero
    m = matriz.split(",")
    for num in m:
        try:
            int(num)
        except ValueError:
            return "Matriz incorrecta"
    salida += ordenarMatrices(m)
    salida = salida.replace("\n", "<br>")
    #se da la opción de lanzar el programa con una matriz aleatoria
    matrizAleatoria = [random.randint(-50,50) for i in range(random.randint(2,200))]
    salida += '<br><a href="' + str(matrizAleatoria)[1:-1] + '">' \
                    'Pulsa para ejecutar el programa con una matriz aleatoria' \
                '</a>'
    salida += "</body></html>"
    return salida

