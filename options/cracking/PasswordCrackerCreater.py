import random
import threading
import time
import string
from datetime import datetime

PLATFORMS = {
    "youtube":  {"symbols": "!@#$%^&*()_-+=[]{}", "min": 8, "max": 20},
    "instagram": {"symbols": "!@#$%&*_-.", "min": 6, "max": 30},
    "tiktok": {"symbols": "!@#$%^&*()_+-=", "min": 8, "max": 24},
    "discord": {"symbols": "!@#$%^&*()_-+=<>?/{}[]", "min": 6, "max": 32}
}

SYMBOL_PACKS = {
    "1": "!@#$%^&*()",
    "2": "[]{}_-+=",
    "3": "<>/?",
    "4": ".,;:!¡¿?*",
    "5": string.punctuation
}

stop_flag = False

def mutate_word(word):
    mutated = ""
    for c in word:
        if c.lower() == "a": mutated += "4"
        elif c.lower() == "e": mutated += "3"
        elif c.lower() == "i": mutated += "1"
        elif c.lower() == "o": mutated += "0"
        elif c.lower() == "s": mutated += "$"
        else:
            mutated += random.choice([c.lower(), c.upper()])
    return mutated

def influence_numbers(word):
    nums = str(len(word))
    nums += str(sum(ord(c) for c in word) % 999)
    nums += "".join(str((ord(c) % 10)) for c in word)
    return nums

def generate_password(base_word, symbols, min_len, max_len, extreme):
    length = random.randint(min_len, max_len)
    mutated = mutate_word(base_word)
    nums = influence_numbers(base_word)
    base_chars = base_word + mutated + nums + symbols
    if extreme:
        base_chars += base_chars[::-1] + base_chars.upper() + base_chars.lower()
    remaining = length - len(base_word) - len(mutated)
    if remaining < 0:
        remaining = random.randint(4, 12)
    chaos = "".join(random.choice(base_chars) for _ in range(remaining))
    pw = base_word + mutated + chaos
    pw = ''.join(random.sample(pw, len(pw)))
    return pw

def worker(base_word, symbols, min_len, max_len, extreme, out):
    while not stop_flag:
        pw = generate_password(base_word, symbols, min_len, max_len, extreme)
        out.append(pw)
        print(pw)

def main():
    print("=== Generador Supremo de Contraseñas Infinitas ===\n")
    for p in PLATFORMS: print(" -", p)
    platform = input("\nPlataforma: ").lower()
    if platform not in PLATFORMS: return
    cfg = PLATFORMS[platform]

    base_word = input("\nPalabra base: ")
    if not base_word.strip(): return

    print("\nOpciones de símbolos especiales:")
    print("1) Símbolos suaves")
    print("2) Símbolos brackets")
    print("3) Símbolos raros")
    print("4) Símbolos de texto")
    print("5) Todos los símbolos")
    print("6) Solo los símbolos permitidos por la plataforma")
    print("7) Ingresar símbolos manualmente")
    pack = input("\nElige opción: ")

    if pack in SYMBOL_PACKS:
        chosen_symbols = SYMBOL_PACKS[pack]
    elif pack == "6":
        chosen_symbols = cfg["symbols"]
    elif pack == "7":
        chosen_symbols = input("Ingresa símbolos manuales: ")
    else:
        chosen_symbols = cfg["symbols"]

    extreme = input("\n¿Modo extremo? (s/n): ").lower() == "s"

    fname = input("\nNombre del archivo (ENTER para automático): ")
    if not fname.strip():
        fname = f"pw-{platform}-{datetime.now().strftime('%Y-%m-%d')}.txt"

    print("\nGenerando infinitamente... CTRL+C para detener.\n")

    results = []
    threads = []
    n_threads = 8

    for _ in range(n_threads):
        t = threading.Thread(target=worker,
                             args=(base_word, chosen_symbols,
                                   cfg["min"], cfg["max"], extreme, results))
        t.start()
        threads.append(t)

    try:
        while True:
            time.sleep(0.05)
    except KeyboardInterrupt:
        global stop_flag
        stop_flag = True
        for t in threads:
            t.join()

    with open(fname, "w") as f:
        for pw in results:
            f.write(pw + "\n")

    print(f"\nArchivo creado: {fname}")
    print("El monstruo duerme… pero tú sabes cómo despertarlo.")

if __name__ == "__main__":
    main()
