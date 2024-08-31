from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

# Configure Chrome options
options = Options()
options.add_argument("--headless")  # Descomente se você não precisar de uma interface gráfica
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

# Aumenta o tempo de espera até a página carregar
wait = WebDriverWait(driver, 15)  # Espera até 15 segundos

try:
    # Aguarda que os elementos estejam presentes na página
    elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[jsname="UWckNb"]')))
    
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
                wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))  # Aguarda o carregamento da página
                
                # Extrai os links .m3u8 dos logs de desempenho
                log_entries = driver.execute_script("return window.performance.getEntriesByType('resource');")
                m3u8_link = None

                for entry in log_entries:
                    if ".m3u8" in entry['name']:
                        print(entry['name'])
                        m3u8_link = entry['name']
                        break
                
                # Adiciona ao arquivo .m3u
                if m3u8_link:
                    file.write(f"#EXTINF:-1,{title}\n")
                    file.write(f"{m3u8_link}\n")
                
                # Volta para a página de resultados
                driver.back()
                wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[jsname="UWckNb"]')))  # Aguarda a página de resultados carregar novamente
            except TimeoutException as e:
                print(f"Tempo esgotado ao processar o link {video_url}: {e}")
            except Exception as e:
                print(f"Erro ao processar o link {video_url}: {e}")

finally:
    # Fecha o navegador
    driver.quit()
