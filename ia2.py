import subprocess
import json
import os

def get_video_details(url):
    """Obtém os detalhes de vídeos individuais ou de playlists, dependendo da URL."""
    try:
        # Primeiro, tenta obter detalhes de vídeo usando youtube-dl
        result = subprocess.run(
            ['youtube-dl', '-j', url],  # Tenta obter detalhes de vídeo ou playlist
            capture_output=True,
            text=True,
            check=True
        )
        details = json.loads(result.stdout)

        # Verifica se a URL é de uma playlist ou de um vídeo
        if isinstance(details, list):  # É uma playlist, retorna a lista de vídeos
            return details
        else:  # Caso contrário, é um único vídeo
            return [details]

    except subprocess.CalledProcessError as e:
        print("youtube-dl falhou, tentando yt-dlp...")
        
        try:
            # Tenta usar yt-dlp
            result = subprocess.run(
                ['yt-dlp', '-j', url],  # Tenta obter detalhes de vídeo ou playlist
                capture_output=True,
                text=True,
                check=True
            )
            details = json.loads(result.stdout)

            # Verifica se a URL é de uma playlist ou de um vídeo
            if isinstance(details, list):  # É uma playlist, retorna a lista de vídeos
                return details
            else:  # Caso contrário, é um único vídeo
                return [details]
        
        except subprocess.CalledProcessError as e:
            print("yt-dlp também falhou.")
            print(f"Erro: {e}")
            return []

def write_m3u_file(details, filename):
    """Escreve os detalhes dos vídeos no formato M3U em um arquivo."""
    with open(filename, 'w', encoding='utf-8') as file:
        # Adiciona o cabeçalho #EXTM3U
        file.write("#EXTM3U\n")
        
        # Adiciona os detalhes dos vídeos no formato M3U
        for entry in details:
            video_url = entry.get('url')
            thumbnail_url = entry.get('thumbnail', 'N/A')
            title = entry.get('title', 'No Title')  # Obtém o título do vídeo

            if video_url:
                # Formata e escreve o título e o URL no formato #EXTINF
                file.write(f"#EXTINF:-1 tvg-logo=\"{thumbnail_url}\",{title}\n")
                file.write(f"{video_url}\n")
            else:
                print(f"URL do vídeo não encontrada para o título: {title}")

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
            all_details.extend(details)  # Acumula os detalhes dos vídeos
        else:
            print(f"Nenhum detalhe encontrado para a URL {url}.")
    
    # Escreve todos os detalhes acumulados em um único arquivo M3U
    filename = 'lista1.M3U'
    write_m3u_file(all_details, filename)
    print(f"Arquivo {filename} criado com sucesso.")

if __name__ == "__main__":
    # Nome do arquivo contendo os URLs
    input_file = 'ia.txt'
    
    # Processa URLs do arquivo
    process_urls_from_file(input_file)
