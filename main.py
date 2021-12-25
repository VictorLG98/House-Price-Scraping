from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import requests
import lxml

BASE_URL = "https://www.zillow.com"

response = requests.get('https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B"pagination"%3A%7B%7D%2C"mapBounds"%3A%7B"west"%3A-122.68910445166016%2C"east"%3A-122.17755354833984%2C"south"%3A37.61555442082665%2C"north"%3A37.934684099448255%7D%2C"mapZoom"%3A11%2C"isMapVisible"%3Atrue%2C"filterState"%3A%7B"price"%3A%7B"max"%3A872627%7D%2C"beds"%3A%7B"min"%3A1%7D%2C"fore"%3A%7B"value"%3Afalse%7D%2C"mp"%3A%7B"max"%3A3000%7D%2C"auc"%3A%7B"value"%3Afalse%7D%2C"nc"%3A%7B"value"%3Afalse%7D%2C"fr"%3A%7B"value"%3Atrue%7D%2C"fsbo"%3A%7B"value"%3Afalse%7D%2C"cmsn"%3A%7B"value"%3Afalse%7D%2C"fsba"%3A%7B"value"%3Afalse%7D%7D%2C"isListVisible"%3Atrue%7D',
                         headers={"Accept-Language":"es-ES,es;q=0.9", "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 OPR/81.0.4196.61"})
respons_text = response.text
soup = BeautifulSoup(respons_text, "html.parser")

all_link_elements = soup.select(".list-card-top a")

all_links = []
for link in all_link_elements:
    href = link["href"]
    if BASE_URL not in href:
        all_links.append(f"{BASE_URL}{href}")
    else:
        all_links.append(href)

# enlaces = []
# for ultag in soup.find_all('ul', {'class': 'photo-cards'}):
#     for litag in ultag.find_all('li'):
#         for item in litag.find_all('a', href=True):
#             if BASE_URL not in item['href']:
#                 item['href'] = BASE_URL + item['href']
#                 enlaces.append(item['href'])
#             else:
#                 enlaces.append(item['href'])

all_address_ele = soup.find_all("address")
all_addresses = [address.get_text().split(" | ")[-1] for address in all_address_ele]

prices = soup.find_all("div", class_="list-card-price")
all_prices = [price.get_text().split("+")[0] for price in prices if "$" in price.text]

s = Service(ChromeDriverManager().install())
driver =webdriver.Chrome(service=s)

for n in range(len(all_links)):
    driver.get("https://docs.google.com/forms/d/e/1FAIpQLSc6QB1t_dUAl_4dIXDST5ljwDPZa_FErYAp5PS6P-EdxAnUcw/viewform?usp=sf_link")
    driver.maximize_window()
    time.sleep(3)

    direcc = driver.find_element(By.CLASS_NAME,
                                 "quantumWizTextinputPaperinputInput")
    precio = driver.find_element(By.XPATH,
                                 '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link = driver.find_element(By.XPATH,
                               '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')

    direcc.send_keys(all_addresses[n])
    precio.send_keys(all_prices[n])
    link.send_keys(all_links[n])
    button.click()


