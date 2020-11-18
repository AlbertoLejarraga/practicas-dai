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
import re

client = MongoClient("mongo", 27017)
dbPokemon = client.pokemon
def obtenerPokemons(filtros, numElems, pagina):
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

    return dbPokemon.samples_pokemon.aggregate(pipeline)
