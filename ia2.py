import subprocess
import json
import os

def get_video_details(url):
    """Obtém os detalhes dos vídeos, incluindo URLs, títulos e thumbnails, usando youtube-dl e, se necessário, yt-dlp."""
    try:
        # Tenta usar youtube-dl
        result = subprocess.run(
            ['youtube-dl', '-j', '--flat-playlist', url],
            capture_output=True,
            text=True,
            check=True
        )
        entries = result.stdout.strip().split('\n')
        details = [json.loads(entry) for entry in entries]
        return details

    except subprocess.CalledProcessError as e:
        print("youtube-dl falhou, tentando yt-dlp...")

        try:
            # Tenta usar yt-dlp
            result = subprocess.run(
                ['yt-dlp', '-j', '--flat-playlist', url],
                capture_output=True,
                text=True,
                check=True
            )
            entries = result.stdout.strip().split('\n')
            details = [json.loads(entry) for entry in entries]
            return details

        except subprocess.CalledProcessError as e:
            print("yt-dlp também falhou.")
            print(f"Erro: {e}")
            return []


def select_best_video_format(formats):
    """Seleciona o melhor formato entre .ts, .mkv, .mp4 ou qualquer outro disponível."""
    print("Verificando formatos disponíveis:")
    # Prioridade de formatos: TS > MKV > MP4 > qualquer outro
    for fmt in formats:
        print(f"Formato encontrado: {fmt.get('ext')}")
        if fmt.get('ext') == 'ts':
            return fmt.get('url')
        elif fmt.get('ext') == 'mkv':
            return fmt.get('url')
        elif fmt.get('ext') == 'mp4':
            return fmt.get('url')
    
    # Caso não encontre nenhum dos formatos preferidos, retorna o primeiro formato disponível
    if formats:
        print("Nenhum formato preferido encontrado, usando o primeiro disponível.")
        return formats[0].get('url')
    
    print("Nenhum formato disponível.")
    return None


def write_m3u_file(details, filename):
    """Escreve os detalhes dos vídeos no formato M3U em um arquivo."""
    with open(filename, 'w', encoding='utf-8') as file:
        # Adiciona o cabeçalho #EXTM3U
        file.write("#EXTM3U\n")

        # Adiciona os detalhes dos vídeos no formato M3U
        for entry in details:
            video_url = entry.get('url')
            formats = entry.get('formats', [])
            thumbnail_url = entry.get('thumbnail', 'N/A')
            title = entry.get('title', 'No Title')  # Obtém o título do vídeo

            # Seleciona a melhor URL de vídeo de acordo com os formatos disponíveis
            if formats:
                video_url = select_best_video_format(formats)

            if video_url:
                # Formata e escreve o título e o URL no formato #EXTINF
                file.write(f"#EXTINF:-1 tvg-logo=\"{thumbnail_url}\",{title}\n")
                file.write(f"{video_url}\n")
            else:
                print(f"URL do vídeo não encontrada para o título {title}.")


def process_urls_from_file(input_file):
    """Lê URLs de um arquivo e processa cada uma para criar um único arquivo M3U."""
    if not os.path.exists(input_file):
        print(f"O arquivo {input_file} não foi encontrado.")
        return

    all_details = []  # Lista para acumular todos os detalhes dos vídeos

    with open(input_file, 'r') as file:
        urls = file.readlines()

    urls = [url.strip() for url in urls if url.strip()]  # Remove espaços em branco e linhas vazias

    for i, url in enumerate(urls):
        print(f"Processando URL {i + 1}: {url}")
        details = get_video_details(url)

        if details:
            all_details.extend(details)  # Acumula os detalhes
        else:
            print(f"Nenhum URL encontrado para a URL {url}.")

    # Escreve todos os detalhes acumulados em um único arquivo M3U
    if all_details:
        filename = 'lista300.M3U'
        write_m3u_file(all_details, filename)
        print(f"Arquivo {filename} criado com sucesso.")
    else:
        print("Nenhum vídeo foi processado. O arquivo M3U não foi criado.")


if __name__ == "__main__":
    # Nome do arquivo contendo os URLs
    input_file = 'ia.txt'

    # Processa URLs do arquivo
    process_urls_from_file(input_file)
