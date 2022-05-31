

########## Request info

# !!!!!!!ОСТОРОЖНО - высирает ТОННУ текста
# info: https://russiannlp.github.io/rugpt-demo/
import json

import requests

__req_link = "https://api.aicloud.sbercloud.ru/public/v1/public_inference/gpt3/predict"

__req_headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36',
    'Content-Type': 'application/json',
    'Accept': '*/*',
    'Origin': 'https://russiannlp.github.io'
}


def __req_body(text):
    return {"text": text}


########## Request info end

def generateSberLargeText(text):
    """
    Генерирует просто ТОННУ текста
    :param text:
    :return:
    """
    body = __req_body(text=text)
    r = requests.post(__req_link, json=body, headers=__req_headers)

    if r.status_code == 200:
        responseJson = json.loads(r.content.decode('utf-8'))
        return responseJson['predictions']
    else:
        print("Ошибка запроса: " + r.request.url + ". Тело: " + body.__str__())
        return "Ошибка " + r.status_code.__str__()