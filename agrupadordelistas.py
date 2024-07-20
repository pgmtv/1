import subprocess
import time
import os
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import yt_dlp




# Configuring Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")

# Instanciando o driver do Chrome
driver = webdriver.Chrome(options=chrome_options)

# URL da página desejada
url_youtube = "https://www.youtube.com/results?search_query=funeral+service&sp=CAISBBABQAE%253D"

# Abrir a página desejada
driver.get(url_youtube)

# Aguardar alguns segundos para carregar todo o conteúdo da página
time.sleep(5)

from selenium.webdriver.common.keys import Keys
for i in range(1):
    try:
        # Find the last video on the page
        last_video = driver.find_element_by_xpath("//a[@class='ScCoreLink-sc-16kq0mq-0 jKBAWW tw-link'][last()]")
        # Scroll to the last video
        actions = ActionChains(driver)
        actions.move_to_element(last_video).perform()
        time.sleep(2)
    except:
        # Press the down arrow key for 50 seconds
        driver.execute_script("window.scrollBy(0, 10000)")
        time.sleep(2)
        
        
# Get the page source again after scrolling to the bottom
html_content = driver.page_source

time.sleep(5)

# Find the links and titles of the videos found
try:
    soup = BeautifulSoup(html_content, "html.parser")
    videos = soup.find_all("a", id="video-title", class_="yt-simple-endpoint style-scope ytd-video-renderer")
    links = ["https://www.youtube.com" + video.get("href") for video in videos]
    titles = [video.get("title") for video in videos]
except Exception as e:
    print(f"Erro: {e}")
finally:
    # Close the driver
    driver.quit()




# Instalando streamlink

subprocess.run(['pip', 'install', 'pytube'])
subprocess.run(['pip', 'install', '--upgrade', 'yt dlp'])

time.sleep(5)
from pytube import YouTube

# Define as opções para o youtube-dl
ydl_opts = {
    'format': 'best',  # Obtém a melhor qualidade

    'write_all_thumbnails': False,  # Não faz download das thumbnails
    'skip_download': True,  # Não faz download do vídeo
}
# Get the playlist and write to file
try:
    with open('./lista1.M3U', 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        for i, link in enumerate(links):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link, download=False)
            if 'url' not in info:
                print(f"Erro ao gravar informações do vídeo {link}: 'url'")
                continue
            url = info['url']
            thumbnail_url = info['thumbnail']
            description = info.get('description', '')[:10]
            title = info.get('title', '')
            f.write(f"#EXTINF:-1 group-title=\"YOUTUBE\" tvg-logo=\"{thumbnail_url}\",{title} - {description}...\n")
            f.write(f"{url}\n")
            f.write("\n")
except Exception as e:
    print(f"Erro ao criar o arquivo .m3u8: {e}")



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

    m3upt_url = "https://gist.github.com/GUAPACHA/ff9cf6435b379c4c550913fdadc8edc4/raw/e5a4f0cc1ebe5a9cd07aa87c9be67004596db1e0/the%2520beatles"
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
    "https://github.com/iptv-org/iptv/blob/master/streams/mx.m3u",    
    "https://github.com/iptv-org/iptv/raw/master/streams/jp.m3u",
    "https://github.com/cqcbrasil/Navez/raw/main/playlist.m3u",
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

