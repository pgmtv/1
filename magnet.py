from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup

# Configure Chrome options
options = Options()
options.add_argument("-headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1280,720")
options.add_argument("--disable-infobars")

# Create the webdriver instance
driver = webdriver.Chrome(options=options)

# Define the base URL
base_url = "https://www.1377x.to/sort-search/CURSO/size/desc/1/"

# Navigate to the base URL
driver.get(base_url)
time.sleep(10)  # Wait for the page to load

# Find and click all the torrent links on the page
torrent_links = []
soup = BeautifulSoup(driver.page_source, 'html.parser')
for tag in soup.find_all('a', href=True):
    href = tag['href']
    if href.startswith('/torrent/'):
        torrent_links.append('https://www.1377x.to' + href)

# List to store all magnet links
all_magnet_links = []

# Iterate over each torrent link
for torrent_link in torrent_links:
    driver.get(torrent_link)
    time.sleep(5)  # Wait for the torrent page to load
    
    # Extract magnet links from the torrent page
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    for tag in soup.find_all('a', class_='torrentdown1', href=True):
        href = tag['href']
        if href.startswith('magnet:?'):
            all_magnet_links.append(href)

# Write the magnet links to a text file
with open('magnet_links.txt', 'w') as file:
    for link in all_magnet_links:
        file.write(f'{link}\n')

# Close the WebDriver
driver.quit()

print("Links magnéticos foram escritos no arquivo magnet_links.txt")
