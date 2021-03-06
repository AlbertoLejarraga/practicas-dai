import re
def apartadoA():
    '''Se genera y prueba la regExp siguiente:
    Identificar cualquier palabra seguida de un espacio y una única letra mayúscula
    (por ejemplo: Apellido N)'''
    salida = ""
    #[a-zA-z]+ [A-Z]==>uno o mas caracteres seguidos por un espacio y un caracter en mayúscula
    #(?!\S)==> siempre que no haya \S, que son todo el conjunto de caracteres no son espacios en blanco,
    #es decir, detecta todos los caracteres considerados espacio (\t\n\r\f\v)
    regExp = "[a-zA-z]+ [A-Z](?!\S)"
    check = "Apellido N HOLA HOLA alberto l Alberto L XXXX X X XXXX Y"
    salida += "Se comprueba la cadena siguiente: '" + check + "'\n"
    salida += str(re.findall(regExp, check)) + "\n"
    return salida

def apartadoB():
    '''Se genera y prueba la regExp siguiente:
    Identificar correos electrónicos válidos (empieza por una expresión genérica y ve refinándola todo lo posible).'''
    #(?<!\S)==>Parecido al anterior pero en este caso "precedido de"
    #([a-zA-Z0-9_.+-]+==>letras mayusculas y minusculas, digitos y esos simbolos una o más veces
    #[a-zA-Z0-9-]+==>detras de la arroba, lo mismo pero solo permitido el guión, una o más veces
    #(\.[a-zA-Z0-9-]+)*==>puede estar o no, si está, es un punto seguido de lo anterior
    #\.[a-z]{2,3}==>termina en . y dos o tres letras
    # (?!\S)==> siempre que no haya \S, que son todo el conjunto de caracteres no son espacios en blanco,
    # es decir, detecta todos los caracteres considerados espacio (\t\n\r\f\v)
    salida = ""
    regExp = "(?<!\S)([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-z]{2,3})(?!\S)"
    check = "albertolej@hotmail.com alejarragar@correo.ugr.es lalala.lalala@.com abcd@la efgh@lala.lele.lili.es ijkl@ijkl@ugr.es mnop@jeje.jejeje.jej .ugr"
    salida += "Se comprueba la cadena siguiente: '" + check + "'\n"
    salida += str([x[0] for x in re.findall(regExp, check)]) + "\n"
    return salida
def apartadoC():
    '''Se genera y prueba la regExp siguiente:
    Identificar números de tarjeta de crédito cuyos dígitos estén separados por - o espacios en blanco cada paquete de cuatro dígitos: 1234-5678-9012-3456 ó 1234 5678 9012 3456.'''
    regExp = "(([0-9]{4}[- ]){3}[0-9]{4})"
    check = "1234-5678-9012-3456 1234 5678 9012 3456 123 456 789 456 11 11 1234 1234 1234 1234"
    salida = ""
    salida += "Se comprueba la cadena siguiente: '" + check + "'\n"
    salida += str([x[0] for x in re.findall(regExp, check)]) + "\n"
    return salida

def ejercicio():
    '''función que realiza el ejercicio 6'''
    salida = "Identificar cualquier palabra seguida de un espacio y una única letra mayúscula (por ejemplo: Apellido N).\n"
    salida += apartadoA()
    salida += "-------------------\n"
    salida += "Identificar correos electrónicos válidos (empieza por una expresión genérica y ve refinándola todo lo posible).\n"
    salida += apartadoB()
    salida += "-------------------\n"
    salida += "Identificar números de tarjeta de crédito cuyos dígitos estén separados por - o espacios en blanco cada paquete de cuatro dígitos: 1234-5678-9012-3456 ó 1234 5678 9012 3456.\n"
    salida += apartadoC()
    return salida

if __name__ == "__main__":
    print(ejercicio())
