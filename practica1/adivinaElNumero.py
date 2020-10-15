#scp -r .\* root@192.168.42.127:/root/dai/practica1/ejercicios
import random

def jugar():
    '''Función que inicia el juego de adivinar el numero'''
    numeroOculto = random.randint(0, 100)
    intentos = 0
    # se comprueba que vayan menos de diez intentos y se pregunta un número
    # si este numero no es el pedido se continua en el bucle
    while (intentos < 10):
        numeroIntro = int(input("Introduzca un número de uno a cien (intento " + str(intentos+1) + "): "))
        if numeroIntro > numeroOculto:
            print("El número buscado es menor")
        elif numeroIntro < numeroOculto:
            print("El número buscado es mayor")
        else:
            break
        intentos += 1
    # se saldra del bucle porque se haya pasado el número de intentos o porque se haya acertado el número
    if intentos >= 10:
        print("Has gastado los diez intentos, el número era " + str(numeroOculto))
    else:
        print("¡Enhorabuena, has acertado con el número " + str(numeroOculto) + "!")
    if (input("Introduce 1 para volver a jugar o 0 para salir") == "1"):
        jugar()


if __name__ == "__main__":
    jugar()
