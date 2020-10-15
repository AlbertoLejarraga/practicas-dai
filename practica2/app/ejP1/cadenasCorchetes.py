import random
def comprobarCadena(cadena):
    '''Función que comprueba si están balanceados los corchetes de la cadena'''
    i = 0
    #se recorre la cadena sumando 1 si se encuentra [ y restando en caso de ]
    #si en algún momento la cuenta da negativo la cadena es incorrecta
    #si se llega al final con un numero mayor a 0 es incorrecta
    #en cualquier otro caso es correcta
    for c in cadena:
        #se comprueba el caracter
        if c =="[":
            i += 1
        else:
            i -= 1
        #se comprueba que la suma sea >=0
        if i < 0:
            return False
    #si el bucle ha acabado, la cuenta debe ser 0 o la cadena será incorrecta
    return i == 0


def checkBalanceados():
    '''Función que genera una cadena de corchetes aleatoria y comprueba si está balanceada'''
    respuesta = input("¿Generar y comprobar nueva cadena? (S/n)")
    #con todo lo que no sea n o N se genera la cadena
    if respuesta != "n" and respuesta != "N":
        longitud = random.randint(2,12)
        cadena = ""
        #se genera la cadena aleatoria
        for i in range(longitud):
            if random.randint(0,1) == 0:
                cadena += "["
            else:
                cadena += "]"
        print(cadena, " ==> ", comprobarCadena(cadena))
    else:
        exit()
if __name__ == "__main__":
    while True:
        checkBalanceados()
