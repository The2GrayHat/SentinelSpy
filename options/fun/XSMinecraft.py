import random

import string

import requests

from threading import Thread, Lock

import time


num_giftcards = 100000000

code_length = 16     

part_length = 4      

num_parts = 4       


characters = string.ascii_uppercase + string.digits  

output_file = "ValidsCodesMinecraft.txt"




lock = Lock()



def generar_codigo():

    parts = [

        ''.join(random.choice(characters) for _ in range(part_length)),

        ''.join(random.choice(characters) for _ in range(part_length)),

        ''.join(random.choice(characters) for _ in range(part_length)),

        ''.join(random.choice(characters) for _ in range(part_length))

    ]

    return '-'.join(parts)



def validar_codigo(codigo):

    url = f"https://api.mojang.com/validate/{codigo}"

    respuesta = requests.get(url)

    if respuesta.status_code == 200:

        return "[+]"  

    else:

        return "[-]"  



def validar_codigo_hilo(codigo):

    resultado = validar_codigo(codigo)

    print(f"{codigo} - {resultado}")


    if resultado == "[+]":

        with lock:

            with open(output_file, "a") as f:

                f.write(codigo + "\n")



def main():

    print(f"Generando y validando {num_giftcards} códigos de Minecraft Premium...")

    

    with open(output_file, "w") as f:

        f.truncate(0)  


    hilos = []

    for _ in range(num_giftcards):

        codigo = generar_codigo()

        hilo = Thread(target=validar_codigo_hilo, args=(codigo,))

        hilos.append(hilo)

        hilo.start()


    for hilo in hilos:

        hilo.join()


    print(f"Se han validado {num_giftcards} códigos. Los válidos se guardaron en '{output_file}'.")



if __name__ == "__main__":

 print("__   __ _____           _                            __ _   ")
print("\ \ / //  ___|         (_)                          / _| |  ")
print(" \ V / \ `--. _ __ ___  _ _ __   ___  ___ _ __ __ _| |_| |_ ")
print(" /   \  `--. \ '_ ` _ \| | '_ \ / _ \/ __| '__/ _` |  _| __|")
print("/ /^\ \/\__/ / | | | | | | | | |  __/ (__| | | (_| | | | |_ ")
print("\/   \/\____/|_| |_| |_|_|_| |_|\___|\___|_|  \__,_|_|  \__|")
print("                                                            ")
print("                                                            ")

print("Este generador fue hecho por XS Clan, porfavor unete a nuestro discord:https://discord.gg/Frybs2bJvv")
print("-------- Generador de Minecraft Premium --------")

usuario_input = input("Para continuar, escriba XS.TOP: ")


if usuario_input == "XS.TOP":

        main()

else:

        print("Entrada incorrecta. El programa se cerrará.")