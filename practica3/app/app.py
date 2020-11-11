from flask import Flask, render_template, flash, session
import random
from app.controller.practica1.ordenacionMatrices import ordenarMatrices
from app.controller.practica1.cribaEratostenes import obtenerPrimos
from app.controller.practica1.fibonacciFichero import fibonacci
from app.controller.practica1.cadenasCorchetes import checkBalanceados
from app.controller.practica1.expresionesRegulares import ejercicio as expresionesRegulares

app = Flask(__name__)
app.secret_key = "clave-secreta-shhh"
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/practica1/ej1/')
def p1Ej1():
    return render_template("practica1/ejercicio1.html")

@app.route('/practica1/ej2/<string:matriz>')
@app.route('/practica1/ej2/')
def p1Ej2(matriz=None):
    #Se comprueba que el formato de la matriz sea correcto, se divide por comas y cada elemento es un entero
    if matriz is None:
        matrizAOrdenar = [random.randint(-50,50) for i in range(random.randint(2,200))]
    else:
        try:
            matrizAOrdenar = [int(i) for i in matriz.split(",")]
        except ValueError:
            return render_template("error.html", error = "La matriz introducida es incorrecta")
    resultado = ordenarMatrices(matrizAOrdenar)
    return render_template("practica1/ejercicio2.html", matrizAOrdenar = matrizAOrdenar, resul = resultado)

@app.route('/practica1/ej3/<int:numeroMax>')
@app.route('/practica1/ej3/')
def ejercicio3(numeroMax=None):
    if numeroMax is None:
        n = random.randint(2,30)
    else:
        #se comprueba que se reciba un número
        try:
            n = int(numeroMax)
            if n < 2:
                return render_template("error.html", error = "Debe introducir un número mayor que 2")
        except ValueError:
            return render_template("error.html", error = "Debe introducir un número mayor que 2")
    return render_template("practica1/ejercicio3.html", numero=n, resul=obtenerPrimos(n))

@app.route('/practica1/ej4/<int:numero>')
@app.route('/practica1/ej4/')
def ejercicio4(numero = None):
    if numero is None:
        numero = random.randint(1,30)
    else:
        #se comprueba que lo introducido sea un número
        try:
            n = int(numero)
            if n<=1:
                return render_template("error.html", error="Compruebe que lo introducido sea realmente un número mayor que 1")
        except ValueError:
            return render_template("error.html", error="Compruebe que lo introducido sea realmente un número mayor que 1")
    numeroPos, serie = fibonacci(numero)
    return render_template("practica1/ejercicio4.html", posicion = numero, numeroPos = numeroPos, serie = serie)

@app.route('/practica1/ej5/')
@app.route('/practica1/ej5/<string:cadena>')
def ejercicio5(cadena=None):
    if cadena is not None:
        for caracter in cadena:
            if caracter not in "[]":
                return render_template("error.html", error="La cadena solo debe contener corchetes")
    return render_template("practica1/ejercicio5.html", resul = checkBalanceados(cadena))

@app.route('/practica1/ej6')
def ejercicio6():
    return render_template("practica1/ejercicio6.html", resul = expresionesRegulares())

@app.route('/practica1/ejParaNota')
def ejercicioParaNota():
    #se generan las distintas figuras posibles con valores aleatorios de tamaño, color, etc.
    figuras={}
    #colores para el Relleno y el Borde
    r = [random.randint(0,255) for i in range(3)]
    b = [random.randint(0,255) for i in range(3)]
    #estilo con valores aleatorios de color y bordes
    estilo = f'fill:rgb({r[0]},{r[1]},{r[2]});stroke-width:{random.randint(0,20)};stroke:rgb({b[0]},{b[1]},{b[2]})'
    figuras["Rectángulo"]= f"<rect x='20', y='20', width='{random.randint(20,80)}%' height='{random.randint(2,80)}' style='{estilo}'/>"
    figuras["Círculo"] = f"<circle cx='200' cy='200' r='{random.randint(25,190)}' style='{estilo}'/>"
    figuras["Elipse"] = f"<ellipse cx='200' cy='200' rx='{random.randint(25,190)}' ry='{random.randint(25,190)}' style='{estilo}'/>"

    #se elige aleatoriamente una figura de las creadas
    figuraSeleccionada = random.choice(list(figuras.keys()))
    return render_template("practica1/ejercicioParaNota.html", nombre = figuraSeleccionada, figura = figuras[figuraSeleccionada])


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
