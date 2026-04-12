import yt_dlp
import re
import subprocess
import sys

def buscar_en_fuente(serie, sitio, limite=100):
    print(f"🔎 Buscando en {sitio}...")
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'extract_flat': 'in_playlist',
    }

    # Query más amplia para atrapar cualquier nombre de capítulo
    query = f"{sitio} {serie} anime OR serie episodio OR capitulo OR temporada"

    resultados = []
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch{limite}:{query}", download=False)
            if "entries" in info:
                for item in info["entries"]:
                    title = item.get("title", "")
                    url = item.get("url", "")
                    if re.search(r"(episodio|cap[ií]tulo|ep|episode)\s*\d+", title, re.IGNORECASE):
                        resultados.append((title, url, sitio))
    except Exception as e:
        print(f"⚠️ Error buscando en {sitio}: {e}")
    return resultados


def reproducir(video_url):
    try:
        subprocess.run(["mpv", video_url])
    except FileNotFoundError:
        print("❌ mpv no está instalado. Instálalo con: sudo apt install mpv")


def main():
    if len(sys.argv) > 1:
        serie = " ".join(sys.argv[1:])
    else:
        serie = input("🎬 Nombre del anime o serie: ").strip()

    plataformas = [
        "youtube",
        "dailymotion",
        "vimeo",
        "bilibili",
        "rutube",
        "ok.ru",
        "reddit"
    ]

    todos_resultados = []
    for sitio in plataformas:
        todos_resultados.extend(buscar_en_fuente(serie, sitio))

    if not todos_resultados:
        print("\n⚠️ No se encontraron capítulos con numeración visible.")
        return

    # Ordenar por número de episodio detectado
    def numero_en_titulo(titulo):
        m = re.search(r"(\d{1,3})", titulo)
        return int(m.group(1)) if m else 9999

    todos_resultados.sort(key=lambda x: numero_en_titulo(x[0]))

    print("\n📜 Episodios encontrados:\n")
    for i, (title, _, sitio) in enumerate(todos_resultados, start=1):
        print(f"{i:02d}. [{sitio}] {title}")

    try:
        eleccion = int(input("\n▶️ Elige un número para reproducir: ")) - 1
        if 0 <= eleccion < len(todos_resultados):
            titulo, url, sitio = todos_resultados[eleccion]
            print(f"\n🎥 Reproduciendo {titulo} ({sitio})...\n")

            # Cada sitio usa URL distinta
            if sitio == "youtube":
                reproducir(f"https://www.youtube.com/watch?v={url}")
            elif sitio == "dailymotion":
                reproducir(f"https://www.dailymotion.com/video/{url}")
            elif sitio == "vimeo":
                reproducir(f"https://vimeo.com/{url}")
            elif sitio == "bilibili":
                reproducir(f"https://www.bilibili.com/video/{url}")
            elif sitio == "rutube":
                reproducir(f"https://rutube.ru/video/{url}")
            elif sitio == "ok.ru":
                reproducir(f"https://ok.ru/video/{url}")
            elif sitio == "reddit":
                reproducir(f"https://reddit.com/{url}")
            else:
                reproducir(url)
        else:
            print("❌ Número fuera de rango.")
    except ValueError:
        print("❌ Entrada inválida.")


if __name__ == "__main__":
    main()
