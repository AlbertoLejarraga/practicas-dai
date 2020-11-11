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
