from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import youtube_dl
import concurrent.futures

# Configure Chrome options
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1280,720")
options.add_argument("--disable-infobars")



# Create the webdriver instance
driver = webdriver.Chrome(options=options)

# URL of the desired page
url_archive = "https://archive.org/details/tvnews?&sort=-date&and[]=languageSorter%3A%22Spanish%22"

# Open the desired page
driver.get(url_archive)

# Wait for the page to load
time.sleep(5)

# Scroll to the bottom of the page
#for _ in range(1):
#    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#    time.sleep(2)

# Find all elements with the specified <a> tags
elements = driver.find_elements(By.CSS_SELECTOR, 'a[title][data-event-click-tracking="GenericNonCollection|ItemTile"]')

# Create a list to store the video URLs and thumbnails
video_infos = []

# Print the href attributes, thumbnails, and add them to video_infos
for element in elements:
    href = element.get_attribute("href")
    if href:
        # Extract the thumbnail URL
        img_element = element.find_element(By.XPATH, './/img')
        thumbnail_src = img_element.get_attribute('src') if img_element else ''
        # Ensure the thumbnail URL is absolute
        if thumbnail_src and not thumbnail_src.startswith('http'):
            thumbnail_src = 'https://archive.org' + thumbnail_src
        video_infos.append((href, thumbnail_src))
        print("Adicionando URL:", href)
        print("Thumbnail:", thumbnail_src)

# Close the webdriver
driver.quit()

# Function to get the direct stream URL and title
def get_stream_info(url):
    ydl_opts = {
        'quiet': True,
        'format': 'best',
        'noplaylist': True,
        'outtmpl': '/dev/null',
        'geturl': True
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        video_title = info_dict.get('title', 'Video Desconhecido')
        stream_url = info_dict.get('url', '')
        return video_title, stream_url

# Generate the EXTINF lines with tvg-logo and URLs
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = list(executor.map(lambda info: get_stream_info(info[0]), video_infos))

# Write the EXTINF formatted lines to a file
with open('lista1.M3U', 'w') as file:
    file.write('#EXTM3U\n')  # Add the EXT3MU header
    for (url, thumbnail), (title, stream_url) in zip(video_infos, results):
        if stream_url:
            tvg_logo = f'tvg-logo="{thumbnail}"' if thumbnail else ''
            file.write(f'#EXTINF:-1 {tvg_logo},{title}\n{stream_url}\n')

print("A playlist M3U foi gerada com sucesso.")


import json
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import yt_dlp

def configure_chrome_options():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    return chrome_options

def initialize_driver(chrome_options):
    return webdriver.Chrome(options=chrome_options)

def fetch_page_source(driver, url, wait_time=5):
    driver.get(url)
    time.sleep(wait_time)
    return driver.page_source

def scroll_to_bottom(driver, scroll_pause_time=2, scroll_count=5):
    for _ in range(scroll_count):
        driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)

def extract_video_info(page_source):
    soup = BeautifulSoup(page_source, "html.parser")
    video_elements = soup.find_all("a", id="video-title")
    links = ["https://www.youtube.com" + video.get("href") for video in video_elements]
    return links

def get_video_metadata(video_url, cookies_file='cookies.json'):
    ydl_opts = {
        'quiet': True,
        'format': 'bestaudio/bestvideo',
        'noplaylist': True,
        'cookiefile': cookies_file  # Usar cookies para autenticação
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(video_url, download=False)
            formats = info.get('formats', [])
            best_format = max(formats, key=lambda x: (x.get('height', 0), x.get('acodec', '')), default={})
            url = best_format.get('url', '')
            title = info.get('title', 'No Title')
            description = info.get('description', '')[:10]
            thumbnail_url = info.get('thumbnail', '')

            if not best_format.get('acodec'):
                print(f"Vídeo {video_url} não possui áudio disponível.")
                url = ''  # Não adicionar vídeo sem áudio

            return {'url': url, 'title': title, 'description': description, 'thumbnail': thumbnail_url}
        except Exception as e:
            print(f"Erro ao listar formatos para o vídeo {video_url}: {e}")
            return None

def create_m3u_playlist(links, filename='./lista1.M3U'):
    try:
        with open(filename, 'a', encoding='utf-8') as f:
            f.write("#EXTM3U\n")
            for link in links:
                metadata = get_video_metadata(link)
                if not metadata or not metadata['url']:
                    print(f"Nenhum formato disponível para o vídeo {link}")
                    continue
                f.write(f"#EXTINF:-1 group-title=\"YOUTUBE\" tvg-logo=\"{metadata['thumbnail']}\",{metadata['title']} - {metadata['description']}...\n")
                f.write(f"{metadata['url']}\n")
                f.write("\n")
    except Exception as e:
        print(f"Erro ao criar o arquivo .m3u: {e}")

def main():
    url_youtube = "https://www.youtube.com/results?search_query=trump&sp=EgJAAQ%253D%253D"
    
    chrome_options = configure_chrome_options()
    driver = initialize_driver(chrome_options)
    
    try:
        page_source = fetch_page_source(driver, url_youtube)
        scroll_to_bottom(driver)
        page_source = driver.page_source

        links = extract_video_info(page_source)
        create_m3u_playlist(links)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()








import requests
from datetime import datetime, timezone, timedelta





# Defina o fuso horário do Brasil
brazil_timezone = timezone(timedelta(hours=-3))

def is_within_time_range(start_time, end_time):
    current_time = datetime.now(brazil_timezone)
    return start_time <= current_time <= end_time

# Horários locais do Brasil para 17h30 e 23h00
start_time_br = datetime.now(brazil_timezone).replace(hour=17, minute=30, second=0, microsecond=0)
end_time_br = datetime.now(brazil_timezone).replace(hour=23, minute=0, second=0, microsecond=0)

# Nome do arquivo de saída
output_file = "lista1.M3U"

if is_within_time_range(start_time_br, end_time_br):
    m3upt_url = "https://github.com/LITUATUI/M3UPT/raw/main/M3U/M3UPT.m3u"
    m3upt_response = requests.get(m3upt_url)

    if m3upt_response.status_code == 200:
        m3upt_lines = m3upt_response.text.split('\n')[:25]

        with open(output_file, "a") as f:
            for line in m3upt_lines:
                f.write(line + '\n')
else:
    with open(output_file, "a") as f:
        f.write("#EXTM3U\n")





#GLOBO


def is_within_time_range(start_time, end_time):
    current_time = datetime.now(brazil_timezone)
    return start_time <= current_time <= end_time

# Horários locais do Brasil para 11h30 e 13h30
start_time_br_morning = datetime.now(brazil_timezone).replace(hour=11, minute=30, second=0, microsecond=0)
end_time_br_morning = datetime.now(brazil_timezone).replace(hour=13, minute=30, second=0, microsecond=0)

# Horários locais do Brasil para 19h00 e 19h45
start_time_br_evening = datetime.now(brazil_timezone).replace(hour=19, minute=0, second=0, microsecond=0)
end_time_br_evening = datetime.now(brazil_timezone).replace(hour=19, minute=45, second=0, microsecond=0)

# Horários locais do Brasil para 17h30 e 23h00
start_time_br = datetime.now(brazil_timezone).replace(hour=5, minute=30, second=0, microsecond=0)
end_time_br = datetime.now(brazil_timezone).replace(hour=8, minute=40, second=0, microsecond=0)

# Nome do arquivo de saída
output_file = "lista1.M3U"

if (is_within_time_range(start_time_br_morning, end_time_br_morning) or 
    is_within_time_range(start_time_br_evening, end_time_br_evening) or
    is_within_time_range(start_time_br, end_time_br)):

    m3upt_url = "https://github.com/strikeinthehouse/1/raw/main/lista2.M3U"
    m3upt_response = requests.get(m3upt_url)

    if m3upt_response.status_code == 200:
        m3upt_lines = m3upt_response.text.split('\n')[:422]

        with open(output_file, "a") as f:
            for line in m3upt_lines:
                f.write(line + '\n')
else:
    with open(output_file, "a") as f:
        f.write("#EXTM3U\n")


import requests

repo_urls = [
    "https://github.com/punkstarbr/STR-YT/raw/main/REALITY'SLIVE.m3u",
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/mx.m3u",    
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/ve.m3u",
    "https://github.com/strikeinthehouse/Navez/raw/main/playlist.m3u"
]



lists = []
for url in repo_urls:
    response = requests.get(url)

    if response.status_code == 200:
        if url.endswith(".m3u"):
            lists.append((url.split("/")[-1], response.text))
        else:
            try:
                contents = response.json()

                m3u_files = [content for content in contents if content["name"].endswith(".m3u")]

                for m3u_file in m3u_files:
                    m3u_url = m3u_file["download_url"]
                    m3u_response = requests.get(m3u_url)

                    if m3u_response.status_code == 200:
                        lists.append((m3u_file["name"], m3u_response.text))
            except requests.exceptions.JSONDecodeError:
                print(f"Error parsing JSON from {url}")
    else:
        print(f"Error retrieving contents from {url}")

lists = sorted(lists, key=lambda x: x[0])

lists = sorted(lists, key=lambda x: x[0])

line_count = 0
with open("lista1.M3U", "a") as f:
    for l in lists:
        lines = l[1].split("\n")
        for line in lines:
            if line_count >= 212:
                break
            if line.strip():  # Pule linhas em branco
                f.write(line + "\n")
                line_count += 1
        if line_count >= 200:
            break




import requests
from datetime import datetime, timezone, timedelta

# Defina o fuso horário do Brasil
brazil_timezone = timezone(timedelta(hours=-3))

def is_within_time_range(start_time, end_time):
    current_time = datetime.now(brazil_timezone)
    return start_time <= current_time <= end_time

# Horários locais do Brasil para 17h30 e 23h00
start_time_br = datetime.now(brazil_timezone).replace(hour=6, minute=00, second=0, microsecond=0)
end_time_br = datetime.now(brazil_timezone).replace(hour=23, minute=59, second=0, microsecond=0)

# Nome do arquivo de saída
output_file = "lista1.M3U"

if is_within_time_range(start_time_br, end_time_br):
    m3upt_url = "https://github.com/punkstarbr/STR-YT/raw/main/lista1.m3u"
    m3upt_response = requests.get(m3upt_url)

    if m3upt_response.status_code == 200:
        m3upt_lines = m3upt_response.text.split('\n')[:500]

        with open(output_file, "a") as f:
            for line in m3upt_lines:
                f.write(line + '\n')
else:
    with open(output_file, "a") as f:
        f.write("#EXTM3U\n")

import requests
from datetime import datetime, timezone, timedelta

# Defina o fuso horário do Brasil
brazil_timezone = timezone(timedelta(hours=-3))

def is_within_time_range(start_time, end_time):
    current_time = datetime.now(brazil_timezone)
    return start_time <= current_time <= end_time

# Horários locais do Brasil para 17h30 e 23h00
start_time_br = datetime.now(brazil_timezone).replace(hour=6, minute=00, second=0, microsecond=0)
end_time_br = datetime.now(brazil_timezone).replace(hour=23, minute=59, second=0, microsecond=0)

# Nome do arquivo de saída
output_file = "lista1.M3U"

if is_within_time_range(start_time_br, end_time_br):
    m3upt_url = "https://github.com/strikeinthehouse/M3UPT/raw/main/M3U/M3UPT.m3u"
    m3upt_response = requests.get(m3upt_url)

    if m3upt_response.status_code == 200:
        m3upt_lines = m3upt_response.text.split('\n')[:500]

        with open(output_file, "a") as f:
            for line in m3upt_lines:
                f.write(line + '\n')
else:
    with open(output_file, "a") as f:
        f.write("#EXTM3U\n")

import requests

# Lista de URLs dos repositórios do GitHub
repo_urls = [
    "https://api.github.com/repos/strikeinthehouse/JCTN/contents",
    "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/ve.m3u"
]

# Função para obter os URLs dos arquivos .m3u de um repositório GitHub
def get_m3u_urls(repo_url):
    m3u_urls = []
    try:
        response = requests.get(repo_url)
        response.raise_for_status()  # Lança uma exceção para erros HTTP
        content = response.json()
        for item in content:
            if item['name'].endswith('.m3u'):
                m3u_urls.append(item['download_url'])
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar {repo_url}: {e}")
    return m3u_urls

# Lista para armazenar todos os URLs dos arquivos .m3u
all_m3u_urls = []

# Itera sobre os URLs dos repositórios e coleta os URLs dos arquivos .m3u
for url in repo_urls:
    if "api.github.com" in url:
        # Se for uma API do GitHub, obtenha os URLs dos arquivos .m3u
        m3u_urls = get_m3u_urls(url)
        all_m3u_urls.extend(m3u_urls)
    elif url.endswith('.m3u'):
        # Se for um arquivo .m3u diretamente, adiciona à lista
        all_m3u_urls.append(url)

# Lista para armazenar o conteúdo dos arquivos .m3u
all_content = []

# Itera sobre os URLs dos arquivos .m3u e coleta o conteúdo de cada um
for url in all_m3u_urls:
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lança uma exceção para erros HTTP
        if response.status_code == 200:
            content = response.text.strip()
            all_content.append(content)
            print(f"Conteúdo do arquivo {url} coletado com sucesso.")
        else:
            print(f"Erro ao acessar {url}: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar {url}: {e}")

# Verifica se há conteúdo para escrever no arquivo .m3u
if all_content:
    with open('lista1.M3U', 'a', encoding='utf-8') as f:
        f.write('#EXTM3U\n')  # Cabeçalho obrigatório para arquivos .m3u
        for content in all_content:
            f.write(content + '\n')

    print('Arquivo lista1.m3u foi criado com sucesso.')
else:
    print('Nenhum conteúdo de arquivo .m3u foi encontrado para escrever.')

import requests

# Lista de URLs dos repositórios do GitHub
repo_urls = [
    "https://api.github.com/repos/punkstarbr/STR-YT/contents"
]

# Função para obter os URLs dos arquivos .m3u de um repositório GitHub
def get_m3u_urls(repo_url):
    m3u_urls = []
    try:
        response = requests.get(repo_url)
        response.raise_for_status()  # Lança uma exceção para erros HTTP
        content = response.json()
        for item in content:
            if item['name'].endswith('.m3u'):
                m3u_urls.append(item['download_url'])
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar {repo_url}: {e}")
    return m3u_urls

# Lista para armazenar todos os URLs dos arquivos .m3u
all_m3u_urls = []

# Itera sobre os URLs dos repositórios e coleta os URLs dos arquivos .m3u
for url in repo_urls:
    if "api.github.com" in url:
        # Se for uma API do GitHub, obtenha os URLs dos arquivos .m3u
        m3u_urls = get_m3u_urls(url)
        all_m3u_urls.extend(m3u_urls)
    elif url.endswith('.m3u'):
        # Se for um arquivo .m3u diretamente, adiciona à lista
        all_m3u_urls.append(url)

# Lista para armazenar o conteúdo dos arquivos .m3u
all_content = []

# Itera sobre os URLs dos arquivos .m3u e coleta o conteúdo de cada um
for url in all_m3u_urls:
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lança uma exceção para erros HTTP
        if response.status_code == 200:
            content = response.text.strip()
            all_content.append(content)
            print(f"Conteúdo do arquivo {url} coletado com sucesso.")
        else:
            print(f"Erro ao acessar {url}: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar {url}: {e}")

# Verifica se há conteúdo para escrever no arquivo .m3u
if all_content:
    with open('lista1.M3U', 'a', encoding='utf-8') as f:
        f.write('#EXTM3U\n')  # Cabeçalho obrigatório para arquivos .m3u
        for content in all_content:
            f.write(content + '\n')

    print('Arquivo lista1.m3u foi criado com sucesso.')
else:
    print('Nenhum conteúdo de arquivo .m3u foi encontrado para escrever.')


def limitar_arquivo_m3u(arquivo_original, arquivo_saida, limite_linhas=900):
    try:
        # Abre o arquivo M3U original para leitura
        with open(arquivo_original, 'r') as file:
            # Lê todas as linhas do arquivo
            linhas = file.readlines()
        
        # Limita as linhas conforme o valor de limite_linhas
        linhas_limitadas = linhas[:limite_linhas]
        
        # Abre o arquivo de saída para escrita
        with open(arquivo_saida, 'w') as file:
            # Escreve as linhas limitadas no novo arquivo
            file.writelines(linhas_limitadas)
        
        print(f"O arquivo {arquivo_original} foi limitado a {limite_linhas} linhas e salvo como {arquivo_saida}.")
    
    except FileNotFoundError:
        print(f"Erro: O arquivo {arquivo_original} não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# Nome do arquivo original e do arquivo de saída
arquivo_original = 'lista1.M3U'
arquivo_saida = 'lista1.M3U'

# Chama a função para limitar o arquivo
limitar_arquivo_m3u(arquivo_original, arquivo_saida)
