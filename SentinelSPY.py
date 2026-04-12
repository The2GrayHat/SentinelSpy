import os
import subprocess
import sys
from colorama import init, Fore, Style

init(autoreset=True)

MODULOS = {
    1: {"nombre": "Osint", "carpeta": "osint"},
    2: {"nombre": "Pages", "carpeta": "pages"},
    3: {"nombre": "Spy", "carpeta": "spy"},
    4: {"nombre": "cracking", "carpeta": "cracking"},
    5: {"nombre": "fun", "carpeta": "fun"},
}

BLANCO = '\033[38;2;255;255;255m'
GRIS_CLARO = '\033[38;2;180;180;180m'
GRIS_OSCURO = '\033[38;2;80;80;80m'
RESET = Style.RESET_ALL

RAW_BANNER = [
 "  ▄▄▄▄▄                                ▄▄   ▄▄▄▄▄     ▄▄▄▄▄▄     ▄▄▄    ",
 "██▀▀▀▀█▄             █▄                ██ ██▀▀▀▀█▄  █▀██▀▀▀█▄  █▀██  ██ ",
 "▀██▄  ▄▀       ▄    ▄██▄▀▀ ▄           ██ ▀██▄  ▄▀    ██▄▄▄█▀    ██  ██ ",
 "  ▀██▄▄  ▄█▀█▄ ████▄ ██ ██ ████▄ ▄█▀█▄ ██   ▀██▄▄     ██▀▀▀      ██  ██ ",
 "▄   ▀██▄ ██▄█▀ ██ ██ ██ ██ ██ ██ ██▄█▀ ██ ▄   ▀██▄  ▄ ██         ██  ██ ",
 "▀██████▀▄▀█▄▄▄▄██ ▀█▄██▄██▄██ ▀█▄▀█▄▄▄▄██ ▀██████▀  ▀██▀         ▀█████▄",
 "                                                                 ▄   ██ ",
 "                                                                 ▀████▀ "
]

def get_gradient_banner():
    colors = [
        (255, 255, 255), (220, 220, 220), (180, 180, 180), (140, 140, 140),
        (100, 100, 100), (80, 80, 80), (60, 60, 60), (40, 40, 40)
    ]
    banner_colored = ""
    for i, line in enumerate(RAW_BANNER):
        r, g, b = colors[i] if i < len(colors) else colors[-1]
        banner_colored += f"\033[38;2;{r};{g};{b}m{line}\n"
    return banner_colored + RESET

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_gradient_line(text):
    print(f"{BLANCO}—{GRIS_CLARO}—{GRIS_OSCURO}—" * (len(text)//3) + RESET)

def get_scripts(modulo_folder):
    directory = os.path.join("options", modulo_folder)
    if not os.path.exists(directory):
        os.makedirs(directory)
        return []
    extensions = ('.py', '.java', '.go', '.sh')
    files = [f for f in os.listdir(directory) if f.endswith(extensions)]
    files.sort()
    return files[:40]

def execute_script(modulo_folder, filename):
    path = os.path.join("options", modulo_folder, filename)
    try:
        if filename.endswith('.py'):
            subprocess.run([sys.executable, path])
        elif filename.endswith('.java'):
            subprocess.run(["java", path])
        elif filename.endswith('.go'):
            subprocess.run(["go", "run", path])
        elif filename.endswith('.sh'):
            subprocess.run(["bash", path])
    except Exception as e:
        print(f"\n{BLANCO}[!] Error: {e}{RESET}")
        input("\nPresiona Enter para continuar...")

def menu_scripts(mod_id):
    mod_info = MODULOS[mod_id]
    while True:
        clear_screen()
        print(get_gradient_banner())
        print(f"{BLANCO}      [+] Módulo: {mod_info['nombre']} - No nos hacemos responsables del mal uso{RESET}")
        print_gradient_line("---------------------------------------------------------")
        scripts = get_scripts(mod_info['carpeta'])
        if not scripts:
            print(f"\n{GRIS_CLARO}    No hay scripts en 'options/{mod_info['carpeta']}'{RESET}")
        else:
            for i, script in enumerate(scripts, 1):
                ext = script.split('.')[-1].upper()
                print(f"    {BLANCO}{i:02d}.{RESET} {GRIS_CLARO}[{ext}]{RESET} {script}")
        print(f"\n{BLANCO}    00.{RESET} Volver al Menú Principal")
        print_gradient_line("---------------------------------------------------------")
        choice = input(f"\n{BLANCO}──({mod_info['nombre']})──>{RESET} ")
        if choice in ['0', '00']: break
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(scripts):
                execute_script(mod_info['carpeta'], scripts[idx])
            else:
                print(f"{GRIS_CLARO}Opción no válida.{RESET}"); input()
        except ValueError:
            print(f"{GRIS_CLARO}Usa números.{RESET}"); input()

def main_menu():
    while True:
        clear_screen()
        print(get_gradient_banner())
        print(f"{BLANCO}      [+] SELECCIÓN DE MÓDULOS{RESET}")
        print_gradient_line("---------------------------------------------------------")
        for key, val in MODULOS.items():
            print(f"    {BLANCO}{key:02d}.{RESET} {GRIS_CLARO}Módulo:{RESET} {val['nombre']}")
        print(f"\n{BLANCO}    00.{RESET} Salir")
        print_gradient_line("---------------------------------------------------------")
        choice = input(f"\n{BLANCO}──(Principal)──>{RESET} ")
        if choice in ['0', '00']:
            print(f"{GRIS_OSCURO}Saliendo...{RESET}")
            break
        try:
            mod_id = int(choice)
            if mod_id in MODULOS:
                menu_scripts(mod_id)
            else:
                print(f"{GRIS_CLARO}Módulo no existe.{RESET}"); input()
        except ValueError:
            print(f"{GRIS_CLARO}Ingresa un número válido.{RESET}"); input()

if __name__ == "__main__":
    if not os.path.exists("options"):
        os.makedirs("options")
    main_menu()
