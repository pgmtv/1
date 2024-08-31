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


# Configure Chrome options
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1280,720")
options.add_argument("--disable-infobars")

# Create the webdriver instance
driver = webdriver.Chrome(options=options)

# URL da página inicial
url = 'https://www.google.com/search?q=integra&sca_esv=1e316cb0aa4d08d4&sca_upv=1&tbas=0&tbs=dur:l,srcf:H4sIAAAAAAAAAKvMLy0pTUrVS87PVSsyB1Pa6Tn5SflgZml-DojWSypSy8svyUzOTCxOTC_1KTM7PSSyGSaQlJqcm5edngzUAABk5f5ZPAAAA&tbm=vid&source=lnt&sa=X&ved=2ahUKEwjg-aqkwJ6IAxWylZUCHVV7CbMQpwV6BAgBECs&biw=1554&bih=956&dpr=1'

# Navega até a página
driver.get(url)

# Aguarda a página carregar
time.sleep(5)  # Ajuste o tempo de espera se necessário

# Coleta todos os links relevantes
elements = driver.find_elements(By.CSS_SELECTOR, 'a[jsname="UWckNb"]')

# Lista para armazenar os URLs e títulos
videos = []

# Armazena todos os links e títulos
for element in elements:
    try:
        video_url = element.get_attribute('href')
        title = element.find_element(By.CSS_SELECTOR, 'h3.LC20lb.MBeuO.DKV0Md').text
        videos.append((video_url, title))
    except Exception as e:
        print(f"Erro ao coletar dados do elemento: {e}")

# Abre o arquivo para escrita
with open('output.m3u', 'w') as file:
    for video_url, title in videos:
        try:
            # Acessa a página do vídeo
            driver.get(video_url)
            time.sleep(10)  # Aguarda a página carregar
            
            # Extrai os links .m3u8 dos logs de desempenho
            log_entries = driver.execute_script("return window.performance.getEntriesByType('resource');")

            for entry in log_entries:
                if ".m3u8" in entry['name']:
                    print(entry['name'])
                    link = entry['name']
                    break
            
            # Adiciona ao arquivo .m3u
            for m3u8_link in m3u8_links:
                file.write(f"#EXTINF:-1,{title}\n")
                file.write(f"{link}\n")
            
            # Volta para a página de resultados
            driver.back()
            time.sleep(5)  # Aguarda a página de resultados carregar novamente
        except Exception as e:
            print(f"Erro ao processar o link {video_url}: {e}")

# Fecha o navegador
driver.quit()








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
    with open(output_path, 'w') as f:
        for link in links:
            response = requests.get(link)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                title = get_title(soup)
                if title:
                    formatted_title = format_video_title(title)
                    # Adiciona a entrada no arquivo M3U
                    f.write(f"{link}\n")

url = "https://www.google.com/search?q=telemundo&sca_esv=e2e26ca2267ebc0e&sca_upv=1&tbs=dur:l,srcf:H4sIAAAAAAAAAB3JQQ6AIAwEwN_10YuRPtKlgLKypRcPvTThOZmLEYE2CRkcWZeBaYAMaq5el-M6QmuIl8dGlTofZmk325849wQv98FRBtk0AAAA&tbm=vid&ei=awLQZrO9DOre1sQPhfe1kQ0&start=20&sa=N&ved=2ahUKEwjznqHHt5mIAxVqr5UCHYV7LdI4ChDw0wN6BAgBEBk&biw=1912&bih=956&dpr=1"
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
with open('pt.txt', 'a') as file:
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
import requests
from bs4 import BeautifulSoup

def get_video_details_youtube(url):
    """Obtém os detalhes dos vídeos usando youtube-dl."""
    try:
        result = subprocess.run(
            ['youtube-dl', '-j', '--flat-playlist', url],
            capture_output=True,
            text=True,
            check=True
        )
        entries = result.stdout.strip().split('\n')
        details = [json.loads(entry) for entry in entries]
        return details

    except subprocess.CalledProcessError:
        return []

def get_video_details_yt_dlp(url):
    """Obtém os detalhes dos vídeos usando yt-dlp."""
    try:
        result = subprocess.run(
            ['yt-dlp', '-j', '--flat-playlist', url],
            capture_output=True,
            text=True,
            check=True
        )
        entries = result.stdout.strip().split('\n')
        details = [json.loads(entry) for entry in entries]
        return details

    except subprocess.CalledProcessError:
        return []

def get_video_details_streamlink(url):
    """Obtém os detalhes dos vídeos usando streamlink."""
    try:
        # Usa o streamlink para obter a URL do stream
        result = subprocess.run(
            ['streamlink', '--stream-url', url, 'best'],
            capture_output=True,
            text=True,
            check=True
        )
        stream_url = result.stdout.strip()
        
        # Faz uma requisição para obter o título da página
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = get_title(soup)
        
        if stream_url and title:
            return [{'url': stream_url, 'title': title, 'thumbnail': 'N/A'}]
        else:
            return []

    except subprocess.CalledProcessError:
        return []
    except requests.RequestException:
        return []

def get_title(soup):
    """Obtém o título do vídeo a partir da BeautifulSoup."""
    title_element = soup.title
    if title_element:
        return title_element.string.strip()
    return "No Title"

def get_video_details(url):
    """Obtém os detalhes dos vídeos usando youtube-dl, yt-dlp ou streamlink."""
    details = get_video_details_youtube(url)
    if details:
        return details

    details = get_video_details_yt_dlp(url)
    if details:
        return details

    details = get_video_details_streamlink(url)
    if details:
        return details

    print(f"Falha ao obter detalhes para a URL {url}.")
    return []

def write_m3u_file(details, filename):
    """Escreve os detalhes dos vídeos no formato M3U em um arquivo."""
    with open(filename, 'a', encoding='utf-8') as file:
        file.write("#EXTM3U\n")
        
        for entry in details:
            video_url = entry.get('url')
            thumbnail_url = entry.get('thumbnail', 'N/A')
            title = entry.get('title', 'No Title')

            if video_url:
                file.write(f"#EXTINF:-1 tvg-logo=\"{thumbnail_url}\",{title}\n")
                file.write(f"{video_url}\n")
            else:
                print("URL do vídeo não encontrada.")

def process_urls_from_file(input_file):
    """Lê URLs de um arquivo e processa cada uma para criar um único arquivo M3U."""
    if not os.path.exists(input_file):
        print(f"O arquivo {input_file} não foi encontrado.")
        return
    
    all_details = []
    
    with open(input_file, 'r') as file:
        urls = file.readlines()
    
    urls = [url.strip() for url in urls if url.strip()]
    
    for i, url in enumerate(urls):
        print(f"Processando URL {i + 1}: {url}")
        details = get_video_details(url)
        
        if details:
            all_details.extend(details)
        else:
            print(f"Nenhum URL encontrado para a URL {url}.")
    
    filename = 'lista1.M3U'
    write_m3u_file(all_details, filename)
    print(f"Arquivo {filename} criado com sucesso.")

if __name__ == "__main__":
    input_file = 'pt.txt'
    process_urls_from_file(input_file)
