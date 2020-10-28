import bs4
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import os
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import random
import urllib.request
from urllib.parse import quote
import transliterator


def edadeal_parser(shop,city):
    city=city.lower()
    city=transliterator.transliterate(city)
    GOOGLE_CHROME_BIN = os.environ.get('GOOGLE_CHROME_BIN')
    CHROMEDRIVER_PATH = os.environ.get('CHROMEDRIVER_PATH')
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
        driver.get("https://edadeal.ru/"+city+"/retailers/" + shop + "?page=" + str(i) + "&segment=beer-cider")
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


def byProductEdadealParser(product,city):
    city = city.lower()
    city = transliterator.transliterate(city)
    GOOGLE_CHROME_BIN = os.environ.get('GOOGLE_CHROME_BIN')
    CHROMEDRIVER_PATH = os.environ.get('CHROMEDRIVER_PATH')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.binary_location = GOOGLE_CHROME_BIN
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=chrome_options)
    url = "https://edadeal.ru/"+city+"/offers"
    print(url)
    driver.get(url)
    search = driver.find_element("class name", "b-header__search-input")
    search.send_keys(product)
    button = driver.find_element("class name", "b-button")
    button.click()
    timeout = 1
    try:
        element_present = EC.presence_of_element_located(("class name", 'b-offer__description'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
    finally:
        print("Page loaded")
    html = driver.page_source
    print(html)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    res = soup.findAll("a", {"class": "p-offers__offer"})
    print(res)
    result = []
    for a in res:
        elem = {
            "description": a.find("div", {"class": "b-offer__description"}).get_text(),
            "market": a.find("div", {"class": "b-offer__retailer-icon"}).get('title'),
            "priceNew": a.find("div", {"class": "b-offer__price-new"}).get_text(),
        }
        result.append(elem)
        print(elem)

    driver.close()
    return result


def randomBeerParser():
    GOOGLE_CHROME_BIN=os.environ.get('GOOGLE_CHROME_BIN')
    CHROMEDRIVER_PATH=os.environ.get('CHROMEDRIVER_PATH')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.binary_location = GOOGLE_CHROME_BIN
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=chrome_options)
    page = str(random.randrange(0, 100))
    url = "https://irecommend.ru/category/alkogol?page={}""&tid=3209".format(page)
    print(url)
    driver.get(url)
    html = driver.page_source
    soup = bs4.BeautifulSoup(html, 'html.parser')
    res = soup.findAll("div", {"class": "ProductTizer plate teaser-item"})
    # print(res)
    rand_beer = random.randrange(0, len(res) - 1)
    a = res[rand_beer]
    url = a.find("div", {"class": "title"}).findChildren('a')[0]
    url ="https://irecommend.ru" +url['href']
    driver.get(url)
    html = driver.page_source
    soup = bs4.BeautifulSoup(html, 'html.parser')
    res = soup.findAll("div", {"class": "mainpic"})[0]
    img = res.find("a", {"class": "photo"})['data-src']
    elem = {
        "name": a.find("div", {"class": "title"}).get_text(),
        "rating": a.find("span", {"class": "average-rating"}).get_text(),
        "image": img,
        "url": url
    }
    driver.close()
    print(elem)
    return elem

