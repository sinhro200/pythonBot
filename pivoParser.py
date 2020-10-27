import json

import requests


def parsePyaterochka():
    response = requests.get(
        "https://skidkaonline.ru/apiv3/products/?limit=30&offset=0&pcategories_ids=414&shop_id=9&city_id=42")
    products = json.loads(response.text)["products"]
    images = []
    for product in products:
        images.append(product['imagefull']['src'])
    return images


def parseMagnit():
    response = requests.get(
        "https://skidkaonline.ru/apiv3/products/?limit=30&offset=0&pcategories_ids=414&shop_id=2&city_id=42")
    products = json.loads(response.text)["products"]
    images = []
    for product in products:
        images.append(product['imagefull']['src'])
    return images


def parseKb():
    beers = {}
    response = requests.get(
        "https://skidkaonline.ru/apiv3/products/?limit=30&offset=0&pcategories_ids=414&shop_id=100&city_id=42")
    products = json.loads(response.text)["products"]
    images = []
    for product in products:
        beers.update({product['name']: product['priceafter']})
    return beers
