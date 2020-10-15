import sys


def obtenerPrimos():
    '''Función que aplica la criba de aristotenes para obtener los primos menores a un numero'''
    #se obtiene el número por parte del usuario y se genera la lista de numeros original
    numeroMax = int(input("Introduce el número máximo"))
    listaNumeros = list(range(2,numeroMax+1))
    #se determina que el número actual a comprobar es el dos y que se esta ante la primera iteración
    numeroActual = 2
    i=1
    #mientras el cuadrado del numero actual no sea mayor que el número máximo indicado
    while pow(numeroActual, 2) <= numeroMax:
        #Se genera una copia de la lista para poder eliminar de esta los no primos (si no se hace una copia el bucle es algo más dificil)
        listaNueva = listaNumeros.copy()
        eliminados = 0
        #para cada elemento de la lista de numeros restantes
        for j, numero in enumerate(listaNumeros[i:]):
            #si el número no es primo con respecto al actual, se elimina de la lista nueva
            if numero % numeroActual == 0:
                listaNueva.pop(j + i - eliminados)
                eliminados += 1
        #se copia la lista a la original, se determina el numero actual y aumenta una iteración
        listaNumeros = listaNueva
        numeroActual = listaNumeros[i]
        i += 1
    #se muestra la lista final
    print(listaNumeros)



if __name__ == "__main__":
    obtenerPrimos()
