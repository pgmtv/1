import subprocess
import os

def stream_video(url):
    """Usa o streamlink para transmitir o vídeo."""
    try:
        # Inicia a transmissão usando streamlink
        subprocess.run(['streamlink', url, 'best'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao tentar transmitir o vídeo: {e}")

def process_urls_from_file(input_file):
    """Lê URLs de um arquivo e processa cada uma para criar transmissões com streamlink."""
    if not os.path.exists(input_file):
        print(f"O arquivo {input_file} não foi encontrado.")
        return
    
    with open(input_file, 'r') as file:
        urls = file.readlines()
    
    urls = [url.strip() for url in urls if url.strip()]  # Remove espaços em branco e linhas vazias
    
    for i, url in enumerate(urls):
        print(f"Processando URL {i + 1}: {url}")
        stream_video(url)  # Chama a função stream_video para iniciar a transmissão
    
    print("Transmissão dos vídeos iniciada.")

if __name__ == "__main__":
    # Nome do arquivo contendo os URLs
    input_file = 'ia.txt'
    
    # Processa URLs do arquivo
    process_urls_from_file(input_file)
