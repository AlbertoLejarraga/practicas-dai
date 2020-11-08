def escribir(numero, fichero):
    '''Función que escribe una linea en un fichero'''
    with open(fichero, "w") as f:
        f.write(numero)
def leerNumeroFichero(fichero):
    '''Función que lee la primera linea de un fichero y la devuelve'''
    with open(fichero) as f:
        linea = f.readline()
    return linea
def fibonacci(n):
    '''Función que obtiene el número en la posicion n de la sucesión de fibonacci
    (Si n no es un número retorna un error que se escribirá después en el fichero)'''
    try:
        n = int(n)
        if n<=1:
            return "Compruebe que lo introducido sea realmente un número mayor que 1"
    except ValueError:
        return "Compruebe que lo introducido sea realmente un número mayor que 1"
    #comprobado que es un número se pasa a obtener el número n de la sucesión de fibonacci
    #se empieza por los números 0 y 1
    a, b = 0, 1
    salida = str(a) + ", "
    #de 2 a n (posiciones 0 y 1 son 0 y 1)
    for i in range(2, n):
        salida += str(b) + ", "
        #a pasa a ser el anterior b y b la suma de ambos en esta iteración
        aux = b
        b += a
        a = aux
    salida += str(b)
    return str(b), salida
if __name__ == "__main__":
    entrada = leerNumeroFichero("entrada.txt")
    numeroFibo = fibonacci(entrada)[0]
    escribir (numeroFibo, "salida.txt")
