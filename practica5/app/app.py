from flask import Flask, render_template, flash, session, request, redirect, url_for, jsonify
import random
import hashlib
from app.controller.practica1.ordenacionMatrices import ordenarMatrices
from app.controller.practica1.cribaEratostenes import obtenerPrimos
from app.controller.practica1.fibonacciFichero import fibonacci
from app.controller.practica1.cadenasCorchetes import checkBalanceados
from app.controller.practica1.expresionesRegulares import ejercicio as expresionesRegulares
from app import model

app = Flask(__name__)
app.secret_key = "clave-secreta-shhh"
#diccionario para almacenar los titulos de las webs
diccURLS = {"/practica1/ej1" : "Ejercicio 1: Adivina el número",
            "/practica1/ej2" : "Ejercicio 2: Ordenación de matrices",
            "/practica1/ej3" : "Ejercicio 3: Criba de Eratóstenes",
            "/practica1/ej4" : "Ejercicio 4: Sucesión de Fibonacci",
            "/practica1/ej5" : "Ejercicio 5: Cadenas de corchetes",
            "/practica1/ej6" : "Ejercicio 6: Expresiones regulares",
            "/practica1/ejParaNota" : "Ejercicio para nota: Figuras SVG",
            "/modificarPerfil" : "Modificar perfil de usuario",
            "/practica4" : "Practica 4: Pokemon GO",
            "/" : "Inicio"}

#se llevan a cabo las siguientes acciones antes de cada petición
@app.before_request
def before_request_callback():
    #solo interesan las llamadas get para almacenar las web visitadas, los formularios vienen siempre por post y no se almacenan
    if request.method == "GET" and "static" not in request.url and "api" not in request.url:#se excluyen las llamadas al directorio static (img, css y js)
        #se detecta cual es el titulo de la página solicitada segun el dicc diccURLS
        for k,v in diccURLS.items():
            if k in request.url:#si se encuentra en el diccionario se crea la variable titulo y se sale
                tituloWeb = v
                break
        if  "listaWebs" not in session:#si es la primera página visitada
            session["listaWebs"] = [[request.url, tituloWeb]]
        else:#se comprueba si no está introducida en la lista, en cuyo caso se añade la primera
            for i, par in enumerate(session["listaWebs"]):
                if par[1] == tituloWeb:#si se encuentra, se saca y se mete la primera
                    session["listaWebs"].pop(i)
            session["listaWebs"] = [[request.url, tituloWeb]] + session["listaWebs"][:4]
        #si el usuario esta logado, se modifica en la base de datos la lista de webs del usuario
        if "nick" in session:
            model.modificarListaVisitadas(session["nick"], session["listaWebs"])

@app.route('/')
def index():
    return render_template("index.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

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

@app.route("/registro", methods = ["POST", "GET"])
def registro():
    if request.method == "GET":
        return render_template("registro.html")
    else:
        nombre = request.form["nombre"]
        apellidos = request.form["apellidos"]
        mail = request.form["mail"]
        nick = request.form["nick"]
        pwd = request.form["pwd"]
        if model.existeUsuario(nick):
            flash("El nick introducido ya existe, prueba con uno nuevo")
            return render_template("registro.html")
        else:
            model.usuarioNuevo(nick, nombre, apellidos, mail, pwd)
            flash (f"Te has registrado con el nick {nick}, ya puedes iniciar sesión")
            return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.pop("nick", None)
    return redirect(request.referrer)

@app.route("/login", methods=["POST"])
def login():
    nick = request.form["nick"]
    pwd = request.form["pwd"]
    if model.existeUsuario(nick) and model.comprobarPwd(nick, pwd):
        session["nick"] = nick
        return redirect(request.referrer)
    else:
        flash("Nombre de usuario o contraseña incorrecto")
        return redirect(url_for("index"))

@app.route("/modificarPerfil", methods = ["GET", "POST"])
def modificarPerfil():
    if request.method == "GET":
        if "nick" in session:
            return render_template("modificarPerfil.html", usuario=model.obtenerDatosUsuario(session["nick"]), nick = session["nick"])
        else:
            flash("Para acceder aquí debes iniciar sesión")
            return redirect(url_for("index"))
    else:
        nombre = request.form["nombre"]
        apellidos = request.form["apellidos"]
        mail = request.form["mail"]
        nick = request.form["nick"]
        pwd = request.form["pwd"]
        if not model.existeUsuario(nick):
            return redirect(url_for("index"))
        else:
            model.modificarUsuario(nick, nombre, apellidos, mail)
            if pwd != "":
                model.modificarPwd(nick, pwd)
            flash ("Datos modificados correctamente")
            return redirect(url_for("index"))

NUM_POKEMONS_PAGINA = 20

@app.route("/practica4")
def practica4():
    #se reciben los parametros pasados por get si hubiera y se determina la pagina segun este parámtetro
    filtros = request.args
    if "page" in request.args:
        if int(request.args["page"]) > 0:
            page = int(request.args["page"])
        else:
            page = 0
    else:
        page = 0
    #se obtienen los datos del modelo
    datosAMostrar = model.obtenerPokemons(filtros, NUM_POKEMONS_PAGINA, page)
    #se renderiza la web con los datos
    return render_template("practica4.html", datos = datosAMostrar, filtros = filtros, url=request.url.split("?page")[0].split("&page")[0], page=page)

@app.route("/borrarPokemon", methods = ["POST"])
def borrarPokemon():
    if model.borrarPokemon(request.form["_id"]):
        flash("Se ha eliminado el pokemon " + request.form["nombre"])
    else:
        flash("No se ha podido eliminar el pokemon, parece que ha habido algún error. Vuelve a intentarlo o contacta con el administrador.")
    return redirect(request.referrer)

@app.route("/modificarPokemon", methods = ["POST"])
def modificarPokemon():
    #se obtienen los datos modificables del formulario y se introducen en un diccionario
    datosModificar = {}
    datosModificar["name"] = request.form["name"]
    datosModificar["img"] = request.form["img"]
    datosModificar["height"] = request.form["height"]
    datosModificar["weight"] = request.form["weight"]
    datosModificar["candy"] = request.form["candy"]
    datosModificar["candy_count"] = request.form["candy_count"]
    datosModificar["egg"] = request.form["egg"]
    datosModificar["spawn_chance"] = request.form["spawn_chance"]
    datosModificar["avg_spawns"] = request.form["avg_spawns"]
    datosModificar["spawn_time"] = request.form["spawn_time"]

    if model.modificarPokemon(request.form["_id"], datosModificar):
        flash("Pokemon de nombre " + datosModificar["name"] + " modificado")
    else:
        flash("No se ha podido modificar el pokemon, parece que ha habido algún error. Vuelve a intentarlo o contacta con el administrador.")
    return redirect(request.referrer)

@app.route("/addPokemon", methods = ["POST"])
def addPokemon():
    #Se obtienen los datos del formularios
    datosAdd = {}
    datosAdd["name"] = request.form["name"]
    datosAdd["img"] = request.form["img"]
    datosAdd["type"] = request.form.getlist("type")
    datosAdd["height"] = request.form["height"] + " m"
    datosAdd["weight"] = request.form["weight"] + " kg"
    datosAdd["candy"] = request.form["candy"]
    datosAdd["candy_count"] = request.form["candy_count"]
    datosAdd["egg"] = request.form["egg"]
    datosAdd["spawn_chance"] = request.form["spawn_chance"]
    datosAdd["avg_spawns"] = request.form["avg_spawns"]
    datosAdd["spawn_time"] = request.form["spawn_time"]
    datosAdd["multipliers"] = [float(request.form["multiplier"])]
    datosAdd["weaknesses"] = request.form.getlist("weaknesses")
    if "next_evolution" in request.form and request.form["next_evolution"] != "":
        datosAdd["next_evolution"] = request.form["next_evolution"]
    if "prev_evolution" in request.form and request.form["prev_evolution"] != "":
        datosAdd["prev_evolution"] = request.form["prev_evolution"]

    if model.addPokemon(datosAdd)[0]:
        flash("Pokemon de nombre " + datosAdd["name"] + " añadido")
    else:
        flash("No se ha podido añadir el pokemon, parece que ha habido algún error. Vuelve a intentarlo o contacta con el administrador.")

    return redirect("/practica4?pagina=" + str(int(model.totalPokemons() / NUM_POKEMONS_PAGINA) + 1))

'''Métodos API REST'''

@app.route("/api/pokemons", methods = ["GET", "POST"])
def api_pokemons_get_post():
    if request.method == "GET":
        #Primero se comprueba si se solicitan datos paginados o no, poniendo los valores por defecto
        pagina = request.args.get("page", 0, int)
        numElems = request.args.get("per_page", model.MAX_ELEMS, int)
        #ahora se obtienen los filtros, si estuvieran
        filtros = {"nombre": request.args.get("name", ""),
                    "tipo": request.args.get("type", ""),
                    "tipoHuevo": request.args.get("egg", ""),
                    "evolucion": request.args.get("evolution", "")}
        #se devuelve un json, cuyos elementos son diccionarios correspondientes a los documentos de mongo sin la clave _id
        datos = model.obtenerPokemons(filtros, numElems, pagina)
        json = jsonify([{k:v for k,v in documento.items() if k != "_id"} for documento in datos])
        return json
    else:#POST
        #se comprueba si se han recibido todos los valores required
        valoresRequired = ["name", "img", "type", "height", "weight", "candy", "candy_count",
                            "egg", "spawn_chance", "avg_spawns", "spawn_time", "multipliers", "weaknesses"]
        datosEntrada = dict(request.get_json())
        for valor in valoresRequired:
            if valor not in datosEntrada.keys() or datosEntrada[valor] == "":
                return {"Error": "Debe introducir, al menos, todos los valores requeridos: " + str(valoresRequired) + ", revise " + valor}
        #ahora se obtienen los datos insertables, los anteriores más estos dos opcionales
        valoresInsertables = valoresRequired + ["next_evolution", "prev_evolution"]
        datosAdd = {}
        for clave in datosEntrada:#se obtienen solo las claves insertables, si hubiera más se descartan
            if clave in valoresInsertables:
                datosAdd[clave] = datosEntrada.get(clave)
        #por último, se modifica el formato de multipliers
        datosAdd["multipliers"] = [datosAdd["multipliers"]]
        resul = model.addPokemon(datosAdd)
        if resul[0]:#si todo es correcto se retorna el id, si no se retorna un error
            return jsonify(resul[1])
        else:
            return {"Error": "No ha podido insertarse el pokemon"}

@app.route("/api/pokemons/<int:id>", methods = ["PUT", "DELETE"])
def api_pokemon_put_delete(id):
    if request.method == "PUT":
        #Se modifica un pokemon según los campos recibidos, comprobados previamente
        valoresModificables = ["name", "img", "height", "weight", "candy", "candy_count", "egg", "spawn_chance", "avg_spawns", "spawn_time"]
        datosEntrada = dict(request.get_json())
        #se obtiene un diccionario con los campos a modificar, si hubiera alguno más se deshecha
        datosModificar = {k:v for k,v in datosEntrada.items() if k in valoresModificables}
        #se modifica y se obtienen los datos modificados
        resulMod = model.modificarPokemonID(id, datosModificar)
        if resulMod is True:
            datos = model.obtenerPokemonID(id)
            datos.pop("_id")
            return datos

        else:
            return {"Error": "No se ha podido modificar el pokemon"}
    else:#DELETE
        if model.borrarPokemonID(id):
            return {"Resultado": "Borrado correcto", "id":id}
        else:
            return {"Error": "No se ha podido eliminar el pokemon"}
        
