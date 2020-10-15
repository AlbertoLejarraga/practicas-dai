from flask import Flask
from app.ejp1.ordenacionMatrices import ordenarMatrices
from app.ejp1.cribaEratostenes import obtenerPrimos
from app.ejp1.fibonacciFichero import fibonacci
from app.ejp1.cadenasCorchetes import checkBalanceados
from app.ejp1.expresionesRegulares import ejercicio as expresionesRegulares
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
    salida += "<h1>Página principal para la práctica 2 de DAI 2020</h1>" \
             "<ul>" \
                "<li><a href='ejercicio2/1,6,7,9,4,3,2,8,5,1'>Ejercicio 2: Ordenación de matrices</a>" \
                "<li><a href='ejercicio3/50'>Ejercicio 3: Criba de Eratóstenes (50)</a>" \
                "<li><a href='ejercicio4/15'>Ejercicio 4: Sucesión de Fibonacci (15)</a>" \
                "<li><a href='ejercicio5'>Ejercicio 5: Comprobación de cadena de corchetes balanceada</a>" \
                "<li><a href='ejercicio6'>Ejercicio 6: Expresiones regulares</a>" \
             "</ul></body></html>"
    return salida

@app.route('/ejercicio2/<string:matriz>')
def ejercicio2(matriz):
    salida = generarCabeceras("Ejercicio 2")
    #Se comprueba que el formato de la matriz sea correcto, se divide por comas y cada elemento es un entero
    m = matriz.split(",")
    for num in m:
        try:
            int(num)
        except ValueError:
            return salida + "<span>Matriz incorrecta</span>"

    salida += "<span>La matriz recibida es: \n[" + matriz + "]\n</span>"
    salida += ordenarMatrices(m)
    salida = salida.replace("\n", "<br>")
    #se da la opción de lanzar el programa con una matriz aleatoria
    matrizAleatoria = [random.randint(-50,50) for i in range(random.randint(2,200))]
    salida += '<br><a href="' + str(matrizAleatoria)[1:-1] + '">' \
                    'Pulsa para ejecutar el programa con una matriz aleatoria' \
                '</a>'
    salida += '<br><a href="../">Ir al inicio</a>'
    salida += "</body></html>"
    return salida

@app.route('/ejercicio3/<int:numeroMax>')
def ejercicio3(numeroMax):
    salida = generarCabeceras("Ejercicio 3")
    #se comprueba que se reciba un número
    try:
        n = int(numeroMax)
        if n < 2:
            return salida + "<span>Es necesario un número mayor de 2</span>"
    except ValueError:
        return salida + "<span>Es necesario un número mayor de 2</span>"
    salida += "<span>Se muestran a continuación los números primos menores a " + str(numeroMax) + " según el algoritmo de la Criba de Eratóstenes</span><br>"
    salida += obtenerPrimos(numeroMax)
    salida += '<br><a href="../">Ir al inicio</a>'
    salida += "</body></html>"
    return salida

@app.route('/ejercicio4/<int:numero>')
def ejercicio4(numero):
    salida = generarCabeceras("Ejercicio 4")
    #La comprobación se hace en el propio programa fibonacci, ya que se leía el dato de manera distinta
    numeroPos, serie = fibonacci(numero)
    salida += "<span>El número que aparece en la posición " + str(numero) + " de la sucesión de Fibonacci es "
    salida += str(numeroPos) + ".</span><br>"
    salida += "<span>Esta es la sucesión completa:</span><br>"
    salida += str(serie)
    salida += '<br><a href="../">Ir al inicio</a>'
    salida += "</body></html>"
    return salida

@app.route('/ejercicio5/')
def ejercicio5():
    salida = generarCabeceras("Ejercicio 5")
    salida += "<span>Se generará aleatoriamente una cadena de corchetes y se mostrará a continuación:</span><br>"
    salida += checkBalanceados()
    salida += '<br><a href="../ejercicio5/">Generar una nueva cadena</a>'
    salida += '<br><a href="../">Ir al inicio</a>'
    salida += "</body></html>"
    return salida


@app.route('/ejercicio6/')
def ejercicio6():
    salida = generarCabeceras("Ejercicio 6")
    salida += "<span>Se realizan las siguientes comprobaciones en base a expresiones regulares:</span><br>"
    salida += "-------------------<br>"
    salida += expresionesRegulares()
    salida += '<br><a href="../">Ir al inicio</a>'
    salida += "</body></html>"
    salida = salida.replace("\n", "<br>")
    return salida

