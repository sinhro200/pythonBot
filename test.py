import bs4
from selenium import webdriver
import os

def edadeal_parser():
    GOOGLE_CHROME_BIN=os.environ.get('GOOGLE_CHROME_BIN')
    CHROMEDRIVER_PATH=os.environ.get('CHROMEDRIVER_PATH')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.binary_location = GOOGLE_CHROME_BIN
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=chrome_options)

    driver.get('https://edadeal.ru/voronezh/offers?segment=beer-cider')
    print(driver.current_url)

    html = driver.page_source
   # print(html)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    res = soup.findAll("a", {"class": "p-offers__offer"})

    driver.close()
    print(res)
    result = []
    for a in res:
         elem = {
             "description": a.find("div", {"class": "b-offer__description"}).get_text(),
              "quantity": a.find("div", {"class": "b-offer__quantity"}).get_text(),
             "priceNew": a.find("div", {"class": "b-offer__price-new"}).get_text(),
             "priceOld": a.find("div", {"class": "b-offer__price-old"}).get_text(),
              "discount": a.find("div", {"class": "b-offer__badge"}).get_text()
         }
         result.append(a.text)
    for elem in result:
        print(elem)
    return result

print(edadeal_parser())

