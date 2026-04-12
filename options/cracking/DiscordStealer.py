import random

import string

import threading

import time

import requests


# URL de la API de Discord para enviar un mensaje

DISCORD_WEBHOOK_URL = "tu api aqui"


# Función para generar contraseñas aleatorias

def generar_contrasena(longitud, incluir_caracteres_especiales):

    caracteres = string.ascii_letters + string.digits

    if incluir_caracteres_especiales:

        caracteres += string.punctuation

    contrasena = ''.join(random.choice(caracteres) for _ in range(longitud))

    return contrasena


# Función para enviar una contraseña a Discord

def enviar_contrasena_a_discord(usuario, contrasena):

    payload = {

        "content": f"**Intento de contrasena para {usuario}:** {contrasena}"

    }

    headers = {

        "Content-Type": "application/json"

    }

    response = requests.post(DISCORD_WEBHOOK_URL, json=payload, headers=headers)

    if response.status_code == 200:

        print(f"[✔] Contraseña enviada: {contrasena}")

    else:

        print(f"[✖] Error al enviar la contraseña: {response.status_code}")


# Función que será ejecutada por cada hilo

def hilo_funcion(usuario, num_threads, incluir_caracteres_especiales):

    while True:

        contrasena = generar_contrasena(10, incluir_caracteres_especiales)

        enviar_contrasena_a_discord(usuario, contrasena)

        time.sleep(0.1)  # Para evitar saturar la API con demasiadas solicitudes


# Función para mostrar el menú de inicio

def mostrar_menu():

    print("Bienvenido al Bruteforcer de Discord")

    usuario = input("Ingresa el nombre de usuario de Discord: ")

    num_threads = int(input("¿Cuántos hilos quieres usar? (recomendado 10-20): "))

    incluir_caracteres_especiales = input("¿Incluir caracteres especiales? (s/n): ").lower() == 's'

    return usuario, num_threads, incluir_caracteres_especiales


# Punto de entrada principal

if __name__ == "__main__":

    usuario, num_threads, incluir_caracteres_especiales = mostrar_menu()

    hilos = []


    # Crear y empezar los hilos

    for _ in range(num_threads):

        h = threading.Thread(target=hilo_funcion, args=(usuario, num_threads, incluir_caracteres_especiales))

        h.start()

        hilos.append(h)


    # Esperar a que todos los hilos terminen (esto es solo para mostrar el proceso, puedes detenerlo manualmente)

    for h in hilos:

        h.join()
