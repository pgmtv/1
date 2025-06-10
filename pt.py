from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os


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
url_archive = "https://tviplayer.iol.pt/ultimos"

# Open the desired page
driver.get(url_archive)

# Wait for the page to load
time.sleep(5)  # Adjust the sleep time if needed to ensure page load

# Find all relevant video links
video_elements = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/video/"]')

# Prepare to write the links to a file
with open("pt.txt", "w") as file:
    for element in video_elements:
        link = element.get_attribute("href")
        # Check if the link is valid and not empty
        if link:
            full_link = f"{link}"
            file.write(full_link + "\n")

# Close the driver
driver.quit()

print("Extração de URLs de páginas de vídeo concluída. As URLs foram salvas em pt.txt")


