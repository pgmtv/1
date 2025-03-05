import os
import json
import internetarchive

def get_video_details(url):
    """Obtém os detalhes dos vídeos armazenados no Internet Archive."""
    try:
        # Usando a biblioteca internetarchive para buscar os metadados do vídeo
        item = internetarchive.get_item(url.split('/')[-1])  # Obtém o item pelo identificador no URL
        files = item.files  # Obtém os arquivos do item

        details = []
        
        # Processa cada arquivo do item
        for file in files:
            if file['format'] == 'Video':  # Filtra arquivos do tipo vídeo
                video_url = file['url']
                title = item.metadata.get('title', 'No Title')  # Obtém o título do vídeo
                thumbnail_url = item.metadata.get('image', 'N/A')  # Obtém a miniatura, se disponível

                details.append({
                    'url': video_url,
                    'title': title,
                    'thumbnail': thumbnail_url
                })
        
        return details

    except Exception as e:
        print(f"Erro ao obter detalhes do vídeo: {e}")
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
    filename = 'lista300.M3U'
    write_m3u_file(all_details, filename)
    print(f"Arquivo {filename} criado com sucesso.")

if __name__ == "__main__":
    # Nome do arquivo contendo os URLs
    input_file = 'ia.txt'
    
    # Processa URLs do arquivo
    process_urls_from_file(input_file)
