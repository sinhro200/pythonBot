import bs4
from selenium import webdriver


def edadeal_parser():
    driver = webdriver.Chrome('D:\chromedriver.exe')
    driver.get('https://edadeal.ru/voronezh/offers?segment=beer-cider')

    html = driver.page_source

    soup = bs4.BeautifulSoup(html, 'html.parser')
    res = soup.findAll("a", {"class": "p-offers__offer"})

    driver.close()

    result = []
    for a in res:
        # elem = {
        #     "description": a.find("div", {"class": "b-offer__description"}).get_text(),
        #     # "quantity": a.find("div", {"class": "b-offer__quantity"}).get_text(),
        #     "priceNew": a.find("div", {"class": "b-offer__price-new"}).get_text(),
        #     # "priceOld": a.find("div", {"class": "b-offer__price-old"}).get_text(),
        #     # "discount": a.find("div", {"class": "b-offer__badge"}).get_text(),
        #     # "market": a.find("div", {"class": "b-offer__dates"}).children.,
        # }
        result.append(a.text)
    # for elem in result:
    #     print(elem)
    return result

#print(edadeal_parser())