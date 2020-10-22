from flask import Flask, url_for, render_template
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
             "<link rel='stylesheet' href='" + url_for('static', filename='general.css') + "'>" \
             "</head>" \
             "<body>"
@app.route('/')
def index():
    salida = generarCabeceras("Inicio")
    salida += "<h1>Página principal para la práctica 2 de DAI 2020</h1>" \
             "<ul>" \
                "<li><a href='" + url_for("ejercicio2", matriz="1,6,7,9,4,3,2,8,5,1") + "'>Ejercicio 2: Ordenación de matrices</a>" \
                "<li><a href='" + url_for("ejercicio3", numeroMax=50) + "'>Ejercicio 3: Criba de Eratóstenes (50)</a>" \
                "<li><a href='" + url_for("ejercicio4", numero=15) + "'>Ejercicio 4: Sucesión de Fibonacci (15)</a>" \
                "<li><a href='" + url_for("ejercicio5") + "'>Ejercicio 5: Comprobación de cadena de corchetes balanceada</a>" \
                "<li><a href='" + url_for("ejercicio6") + "'>Ejercicio 6: Expresiones regulares</a>" \
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
    salida += '<br><a href="' + url_for("ejercicio2", matriz=str(matrizAleatoria)[1:-1]) + '">' \
                    'Pulsa para ejecutar el programa con una matriz aleatoria' \
                '</a>'
    salida += '<br><a href=' + url_for("index") + '>Ir al inicio</a>'
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
    salida += '<br><a href=' + url_for("index") + '>Ir al inicio</a>'
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
    salida += '<br><a href=' + url_for("index") + '>Ir al inicio</a>'
    salida += "</body></html>"
    return salida

@app.route('/ejercicio5/')
def ejercicio5():
    salida = generarCabeceras("Ejercicio 5")
    salida += "<span>Se generará aleatoriamente una cadena de corchetes y se mostrará a continuación:</span><br>"
    salida += checkBalanceados()
    salida += '<br><a href=' + url_for("ejercicio5") + '>Generar una nueva cadena</a>'
    salida += '<br><a href=' + url_for("index") + '>Ir al inicio</a>'
    salida += "</body></html>"
    return salida


@app.route('/ejercicio6/')
def ejercicio6():
    salida = generarCabeceras("Ejercicio 6")
    salida += "<span>Se realizan las siguientes comprobaciones en base a expresiones regulares:</span><br>"
    salida += "-------------------<br>"
    salida += expresionesRegulares()
    salida += '<br><a href=' + url_for("index") + '>Ir al inicio</a>'
    salida += "</body></html>"
    salida = salida.replace("\n", "<br>")
    return salida

@app.route('/ejercicio-para-nota/')
def ejercicioParaNota():
    salida = generarCabeceras("Ejercicio para nota")
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

    #se genera el html con un marco svg general y una figura aleatoria dentro
    figuraSeleccionada = random.choice(list(figuras.keys()))
    salida += f'''  <h1>{figuraSeleccionada}</h1>
                    <svg width='400' height='400'>
                        {figuras[figuraSeleccionada]}
                    </svg>'''
    salida += '<br><a href=' + url_for("index") + '>Ir al inicio</a>'
    salida += '''
                </body>
                </html>
                '''
    return salida

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
