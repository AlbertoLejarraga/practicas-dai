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
    except ValueError:
        return "Compruebe el fichero, no es un número"
    #comprobado que es un número se pasa a obtener el número n de la sucesión de fibonacci
    #se empieza por los números 0 y 1
    a, b = 0, 1
    print(a, end = ", ")
    #de 2 a n (posiciones 0 y 1 son 0 y 1)
    for i in range(2, n):
        print(b, end = ", ")
        #a pasa a ser el anterior b y b la suma de ambos en esta iteración
        aux = b
        b += a
        a = aux
    print(b)
    return str(b)
if __name__ == "__main__":
    entrada = leerNumeroFichero("entrada.txt")
    numeroFibo = fibonacci(entrada)
    escribir (numeroFibo, "salida.txt")
