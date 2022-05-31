import requests
import json

########## Request info

# info https://porfirevich.ru/
__req_link = "https://pelevin.gpt.dobro.ai/generate/"

__req_headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36',
    'Content-Type': 'application/json',
    'Accept': '*/*',
    'Origin': 'https://porfirevich.ru'
}


def __req_body(prompt, length=30):
    return {"prompt": prompt, "length": length}


########## Request info end

def generatePelevin(prompt, length=30) -> list:
    """
    :return Список возможных продолжений, чаще всего их 3
    :rtype: list
    """
    body = __req_body(prompt=prompt, length=length)
    r = requests.post(__req_link, json=body, headers=__req_headers)
    if r.status_code == 200:
        responseJson = json.loads(r.content.decode('utf-8'))
        return responseJson['replies']
    else:
        print("Ошибка запроса: " + r.request.url + ". Тело: " + body)
        return "Ошибка " + r.status_code.__str__()
