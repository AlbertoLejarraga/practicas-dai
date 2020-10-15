import random
from time import perf_counter

def burbuja(matriz):
    '''Función que aplica el algoritmo de ordenación burbuja a una matriz unidimensional'''
    #se empieza por el indice 1 de la matriz
    i=1
    ordenado = False
    #Mientras no esté ordenada y con i de 0 al tamaño
    while(i<len(matriz) and not ordenado):
        ordenado = True
        #cada iteracion i, conlleva una iteración j menos
        #desde 0 hasta la longitud de la matriz menos el numero de iteraciones i
        for j in range(len(matriz) - i):
            #si los numeros en las posiciones j y j+1 estan desordenados
            if matriz[j]>matriz[j+1]:#se intercambian los valores
                ordenado = False
                aux = matriz[j+1]
                matriz[j+1] = matriz[j]
                matriz[j] = aux
        i += 1
    return matriz

def merge(izq, der):
    '''Parte del algoritmo merge sort'''
    resul = []
    #indices del bucle para la lista izq y der
    i, d = 0, 0
    #hasta que alguna de las dos listas terminen
    while (i<len(izq) and d<len(der)):
        #se añade el elemento correspondiente, el de la lista de la derecha o el de la izuqierda
        if(izq[i]<=der[d]):
            resul += [izq[i]]
            i += 1
        else:
            resul += [der[d]]
            d += 1
    #en función de si se ha terminado con una u otra lista, se añade la parte restante
    if (i<len(izq)):
        resul += izq[i:]
    elif (d<len(der)):
        resul += der[d:]
    return resul


def mergeSort(matriz):
    '''Función que aplica el algoritmo de ordenación mezcla o merge sort a una matriz unidimensional'''
    if (len(matriz) <=1):
        return matriz
    else:
        #se parte la matriz en dos mitades
        izq = matriz[0:int(len(matriz)/2)]
        der = matriz[int(len(matriz)/2):]
        #se ordenan recursivamente
        izq = mergeSort(izq)
        der = mergeSort(der)
        #se el ultimo elemento de la parte izquierda no es mayor que el primero de la derecha
        if (izq[-1] <= der[0]):
            return izq + der
        #si fuera mayor, hay que ordenar
        return merge(izq, der)


def ordenar(matriz, algoritmo):
    '''Función llamada para ordenar una matriz según un algoritmo'''
    matrizCopia = matriz.copy()
    if algoritmo == "burbuja":
        return burbuja(matrizCopia)
    elif algoritmo == "mergeSort":
        return mergeSort(matrizCopia)
    else:
        return matriz

def ordenarMatrices(matriz=None):
    '''Función que realiza el ejercicio 2 de ordenación de matrices'''
    salida = ""
    if matriz is None:
        #se genera una matriz de números de tamaño dado por el usuario
        tamano = int (input("Introduzca el tamaño de la matriz"))
        if tamano > 1:
            matriz = [random.randint(-3*tamano, 3*tamano) for i in range(tamano)]
            salida += "Esta es la matriz: \n"
            salida += str(matriz)
        else:
            salida += "\nTamaño incorrecto\n"
            exit()
    else:
        matriz = [int(elem) for elem in matriz]
    #se determinan los algoritmos de ordenacion
    algoritmos = ["burbuja", "mergeSort"]
    for alg in algoritmos:
        salida += "--------------\n"
        salida += "Probando el algoritmo '" + alg + "' para la matriz...\n"
        ini = perf_counter()
        matrizOrdenada = ordenar(matriz, alg)
        fin = perf_counter()
        salida += "El tiempo transcurrido en segundos es de " + str(fin-ini) +"\n"
        salida += "Matriz ordenada: \n"
        salida += str(matrizOrdenada)
        salida += "\n--------------"
    return salida
if __name__ == "__main__":
    print(ordenarMatrices())
