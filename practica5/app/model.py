from pickleshare import *
import hashlib

db = PickleShareDB("dbUsuarios")
def existeUsuario(nick):
    return nick in db
def usuarioNuevo(nick, nombre, apellidos, mail, pwd):
    db[nick] = {"nombre":nombre, "apellidos":apellidos, "mail": mail, "pwd":hashlib.sha256(pwd.encode('utf-8')).hexdigest()}
def comprobarPwd(nick, pwd):
    return db[nick]["pwd"] == hashlib.sha256(pwd.encode('utf-8')).hexdigest()
def obtenerDatosUsuario(nick):
    return db[nick]
def modificarUsuario(nick, nombre, apellidos, mail):
    db[nick]["nombre"] = nombre
    db[nick]["apellidos"] = apellidos
    db[nick]["mail"] = mail
    db[nick] = db[nick]

def modificarPwd(nick, pwd):
    db[nick]["pwd"] =  hashlib.sha256(pwd.encode('utf-8')).hexdigest()
    db[nick] = db[nick]
def modificarListaVisitadas(nick, lista):
    db[nick]["listaVisitadas"] = lista[:5]
    db[nick] = db[nick]
def obtenerListaWebsUsuario(nick):
    if "listaVisitadas" in db[nick]:
        return db[nick]["listaVisitadas"]
    else:
        return []


'''Mongo'''
from pymongo import MongoClient
from bson.objectid import ObjectId
import re

client = MongoClient("mongo", 27017)
dbPokemon = client.pokemon
MAX_ELEMS = 10000
def obtenerPokemons(filtros={}, numElems=MAX_ELEMS, pagina=0):
    #para el caso de que no se especifiquen parametros se devuelve todo
    if filtros == {} and numElems == MAX_ELEMS and pagina == 0:
        return dbPokemon.samples_pokemon.find({}, limit=MAX_ELEMS)
    filtrosAgg = {}
    if "tipo" in filtros and filtros["tipo"]!="": filtrosAgg["type"]=filtros["tipo"]
    if "tipoHuevo" in filtros and filtros["tipoHuevo"]!="": filtrosAgg["egg"]=filtros["tipoHuevo"]
    if "evolucion" in filtros and filtros["evolucion"]!="": filtrosAgg["evolucion"]=filtros["evolucion"]
    if "nombre" in filtros and filtros["nombre"]!="":
        filtrosAgg["name"] = {
                                                                                '$regex': re.compile(r"{}(?i)".format(filtros["nombre"]))
                                                                            }

    pipeline = [
    {#addfields para añadir el campo evolucion
        '$addFields': {
            'evolucion': {
                '$cond': {#si tiene 0 evoluciones previas, es la primera evolucion
                    'if': {
                        '$eq': [
                            {
                                '$size': {
                                    '$ifNull': [
                                        '$prev_evolution', []
                                    ]
                                }
                            }, 0
                        ]
                    },
                    'then': '1',
                    'else': {
                        '$cond': {
                            'if': {#si tiene 1 evolucion previa es la segunda evolucion
                                '$eq': [
                                    {
                                        '$size': {
                                            '$ifNull': [
                                                '$prev_evolution', []
                                            ]
                                        }
                                    }, 1
                                ]
                            },
                            'then': '2',
                            'else': '3'#si tiene 2 evoluciones previas es la tercera evolucion
                        }
                    }
                }
            }
        }
    }, {
        '$match': filtrosAgg#se hace match de los filtros
    }, {
        '$skip': pagina*numElems#se saltan los elementos segun el numero de pagina y el numero de pokemons a mostrar
    }, {
        '$limit': numElems#se limita el numero de pokemons a mostrar
    }
]
    resul = dbPokemon.samples_pokemon.aggregate(pipeline)
    return list(resul)
def borrarPokemon(id):
    resul = dbPokemon.samples_pokemon.delete_one({"_id":ObjectId(id)})
    return resul.deleted_count == 1
def modificarPokemon(id, datosModificar):
    resul = dbPokemon.samples_pokemon.update_one({"_id":ObjectId(id)}, {"$set" : datosModificar})
    return resul.modified_count == 1
def addPokemon(datosAdd):
    #lo primero que se necesita es obtener el valor de id (no _id) del último pokemon,
    #para que el id del nuevo pokemon sea uno más que este
    maxId = list(dbPokemon.samples_pokemon.aggregate([
                                                    {
                                                        '$group': {
                                                            '_id': None,
                                                            'maxId': {
                                                                '$max': '$id'
                                                            }
                                                        }
                                                    }
                                                ]))[0]
    #se añaden los valores de id y num a datosAdd, el segundo parte del primero
    datosAdd["id"] = int(maxId["maxId"]) + 1
    datosAdd["num"] = str(int(maxId["maxId"]) + 1)
    #ahora se obtiene el nombre del pokemon introducido como next_evolution y prev_evolution

    if "next_evolution" in datosAdd:#se comprueba si se ha mandado por formulario
        next_evolution = dbPokemon.samples_pokemon.find_one({"id" : int(datosAdd["next_evolution"])})
        if next_evolution is not None:#se comprueba si lo mandado por form esta en la bd, si esta se monta el dict
            datosAdd["next_evolution"] = [{"num" : next_evolution["num"], "name" : next_evolution["name"]}]
        else:#si no, se elimina el elemento del dict
            datosAdd.pop("next_evolution", None)
    if "prev_evolution" in datosAdd:
        prev_evolution = dbPokemon.samples_pokemon.find_one({"id" : int(datosAdd["prev_evolution"])})
        if prev_evolution is not None:
            datosAdd["prev_evolution"] = [{"num" : prev_evolution["num"], "name" : prev_evolution["name"]}]
        else:
            datosAdd.pop("prev_evolution", None)
    id_insertado = dbPokemon.samples_pokemon.insert_one(datosAdd).inserted_id

    return id_insertado != None
def totalPokemons():
    return dbPokemon.samples_pokemon.count()
