import yt_dlp
import json
import os

def get_video_details(url):
    """Obtém os detalhes dos vídeos, incluindo URLs, títulos e thumbnails, usando yt-dlp para playlists e canais."""
    try:
        ydl_opts = {
            'quiet': True,  # Desativa a saída do terminal
            'extract_flat': False,  # Não apenas extrair links, mas os detalhes completos dos vídeos
            'force_generic_extractor': False,  # Tenta usar o extrator correto
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extrai informações do URL fornecido (pode ser playlist, canal ou vídeo individual)
            result = ydl.extract_info(url, download=False)
            
            # Se for uma playlist ou canal, 'entries' contém todos os vídeos
            if 'entries' in result:
                return result['entries']
            else:
                # Se for um único vídeo, retornamos ele como uma lista com um único elemento
                return [result]
    
    except Exception as e:
        print(f"Erro ao obter detalhes: {e}")
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
                print("URL do vídeo não encontrada.")

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
    filename = 'lista1.M3U'
    write_m3u_file(all_details, filename)
    print(f"Arquivo {filename} criado com sucesso.")

if __name__ == "__main__":
    # Nome do arquivo contendo os URLs
    input_file = 'ia.txt'
    
    # Processa URLs do arquivo
    process_urls_from_file(input_file)
