from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import streamlink

# Configure Chrome options
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1280,720")
options.add_argument("--disable-infobars")

# Create the webdriver instance
driver = webdriver.Chrome(options=options)

def get_title(soup):
    title_element = soup.title
    if title_element:
        return title_element.string.strip()
    return None

def format_video_title(title):
    formatted_title = f"{title.replace('/', '_')}"
    return formatted_title

def extract_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = []
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.startswith('http') and not href.startswith('https://www.youtube.com') or href.startswith('https://secure2.rtve.es'):
            links.append(href)
    return links

def write_m3u_file(links, output_path):
    with open(output_path, 'a') as f:
        for link in links:
            response = requests.get(link)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                title = get_title(soup)
                if title:
                    formatted_title = format_video_title(title)
                    # Adiciona a entrada no arquivo M3U
                    f.write(f"{link}\n")

url = "https://www.rtve.es/play/arquivo/"
driver.get(url)

for i in range(2):
    try:
        # Find the last video on the page
        last_video = driver.find_element(By.XPATH, "//a[@class='ScCoreLink-sc-16kq0mq-0 jKBAWW tw-link'][last()]")
        # Scroll to the last video
        actions = ActionChains(driver)
        actions.move_to_element(last_video).perform()
        time.sleep(2)
    except:
        # Scroll down the page
        driver.execute_script("window.scrollBy(0, 10000)")
        time.sleep(2)

try:
    body = driver.find_element(By.TAG_NAME, "body")
    body.send_keys(Keys.END)
    time.sleep(5)
    links = []
    for a_tag in driver.find_elements(By.CSS_SELECTOR, "a[href^='http']"):
        href = a_tag.get_attribute("href")
        if href and not href.startswith("https://www.youtube.com"):
            links.append(href)
except NoSuchElementException:
    print("Failed to find the 'body' element.")

driver.quit()

# Definindo o caminho para a pasta raiz
m3u_file_path = os.path.join(os.getcwd(), "pt.txt")

# Criação do arquivo M3U na pasta raiz
write_m3u_file(links, m3u_file_path)

print(f"Arquivo M3U foi criado: {m3u_file_path}")



from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time


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
url_archive = "https://tviplayer.iol.pt/videos/ultimos/1/canal:"

# Open the desired page
driver.get(url_archive)

# Wait for the page to load
time.sleep(5)  # Adjust the sleep time if needed to ensure page load

# Find all relevant video links
video_elements = driver.find_elements(By.CSS_SELECTOR, 'a.item')

# Prepare to write the links to a file
with open('pt.txt', 'w') as file:
    for element in video_elements:
        link = element.get_attribute('href')
        # Check if the link is valid and not empty
        if link:
            full_link = f"{link}"
            file.write(full_link + '\n')

# Close the driver
driver.quit()



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

def write_m3u_file(details, filename):
    """Escreve os detalhes dos vídeos no formato M3U em um arquivo."""
    with open(filename, 'a', encoding='utf-8') as file:
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
    input_file = 'pt.txt'
    
    # Processa URLs do arquivo
    process_urls_from_file(input_file)
