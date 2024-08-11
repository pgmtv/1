import subprocess
import json
import re

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

def filter_and_write_m3u_file(details, filename='lista1.M3U'):
    """Filtra URLs com extensões .ts e .mkv e escreve os detalhes no formato M3U em um arquivo."""
    with open(filename, 'w', encoding='utf-8') as file:
        # Adiciona o cabeçalho #EXTM3U
        file.write("#EXTM3U\n")
        
        # Define uma regex para verificar extensões de vídeo
        video_ext_regex = re.compile(r'\.(ts|mkv)$', re.IGNORECASE)
        
        # Filtra e escreve os detalhes dos vídeos no formato M3U
        for entry in details:
            video_url = entry.get('url')
            thumbnail_url = entry.get('thumbnail', 'N/A')
            title = entry.get('title', 'No Title')  # Obtém o título do vídeo

            if video_url and video_ext_regex.search(video_url):
                # Formata e escreve o título e o URL no formato #EXTINF
                file.write(f"#EXTINF:-1 tvg-logo=\"{thumbnail_url}\", {title}\n")
                file.write(f"{video_url}\n")
            else:
                if video_url:
                    print(f"URL do vídeo {video_url} não tem a extensão .ts ou .mkv e foi ignorada.")

if __name__ == "__main__":
    # URL da coleção do Archive.org
    archive_url = 'https://archive.org/details/sportv-4-02.09.21-16.42-0/SPORTV+4+02.09.21+16.42_0.ts'
    
    # Obtém os detalhes dos vídeos
    details = get_video_details(archive_url)
    
    # Filtra os links e escreve os detalhes no arquivo M3U
    if details:
        filter_and_write_m3u_file(details)
        print("Arquivo lista1.M3U criado com sucesso.")
    else:
        print("Nenhum URL encontrado.")
