from flask import Flask, render_template
import random
from app.controller.practica1.ordenacionMatrices import ordenarMatrices
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/practica1/ej2/<string:matriz>')
def p1Ej2(matriz):
    #Se comprueba que el formato de la matriz sea correcto, se divide por comas y cada elemento es un entero
    if matriz == "random":
        matrizAOrdenar = [random.randint(-50,50) for i in range(random.randint(2,200))]
    else:
        matrizAOrdenar = matriz.split(",")
        for num in matrizAOrdenar:
            try:
                int(num)
            except ValueError:
                return render_template("error.html", error = "La matriz introducida es incorrecta")
    resultado = ordenarMatrices(matrizAOrdenar)
    print("resul" + resultado, flush=True)
    return render_template("practica1/ejercicio2.html", matrizAOrdenar = str(matrizAOrdenar), resul = resultado)



@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
