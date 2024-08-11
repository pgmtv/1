!pip install youtube-dl yt-dlp


import subprocess
import json

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

def print_extinf(details):
    """Exibe os detalhes dos vídeos no formato #EXTINF, incluindo título e thumbnail como tvg-logo, e URL na linha de baixo."""
    for entry in details:
        video_url = entry.get('url')
        thumbnail_url = entry.get('thumbnail', 'N/A')
        title = entry.get('title', 'No Title')  # Obtém o título do vídeo

        if video_url:
            # Formata e exibe o título e o URL no formato #EXTINF
            print(f"#EXTINF:-1 tvg-logo=\"{thumbnail_url}\", {title}")
            print(video_url)
        else:
            print("URL do vídeo não encontrada.")

if __name__ == "__main__":
    # URL da coleção do Archive.org
    archive_url = 'https://archive.org/details/sportv-2-02.02.22-08.08'
    
    # Obtém os detalhes dos vídeos
    details = get_video_details(archive_url)
    
    # Exibe os detalhes no formato #EXTINF
    if details:
        print_extinf(details)
    else:
        print("Nenhum URL encontrado.")
