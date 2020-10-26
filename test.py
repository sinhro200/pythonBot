import bs4
from selenium import webdriver
import os


def edadeal_parser(shop):
    GOOGLE_CHROME_BIN=os.environ.get('GOOGLE_CHROME_BIN')
    CHROMEDRIVER_PATH=os.environ.get('CHROMEDRIVER_PATH')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.binary_location = GOOGLE_CHROME_BIN
    i = 1
    discounts = []
    while True:
        print("page" + str(i))
        driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=chrome_options)
        driver.get("https://edadeal.ru/voronezh/retailers/" + shop + "?page=" + str(i) + "&segment=beer-cider")
        print(driver.current_url)
        html = driver.page_source

        soup = bs4.BeautifulSoup(html, 'html.parser')
        res = soup.findAll("a", {"class": "p-retailer__offer"})

        result = []
        for a in res:
            elem = {
                "priceNew": a.find("div", {"class": "b-offer__price-new"}).get_text(),
                "description": a.find("div", {"class": "b-offer__description"}).get_text(),
                # "discount": a.find("div", {"class": "b-offer__badge"}).get_text(),
                # "market": a.find("div", {"class": "b-offer__dates"}).children.,
            }
            result.append(elem)
            print(elem)
        discounts.extend(result)
        if result == []:
            return discounts
        i += 1
        driver.close()


