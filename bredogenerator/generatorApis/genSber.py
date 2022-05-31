import json

import requests

########## Request info


# info: https://huggingface.co/sberbank-ai/rugpt3large_based_on_gpt2
__req_link_large = "https://api-inference.huggingface.co/models/sberbank-ai/rugpt3large_based_on_gpt2"

# info: https://huggingface.co/sberbank-ai/rugpt3small_based_on_gpt2
__req_link_small = "https://api-inference.huggingface.co/models/sberbank-ai/rugpt3small_based_on_gpt2"
__req_headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36',
    'Content-Type': 'application/json',
    'Accept': '*/*',
    'Origin': 'https://huggingface.co'
}


def __req_body(prompt):
    return {"inputs": prompt}


########## Request info end


# Обычно долго подгружается, то есть несколько первых запросов будут падать
def generateSber(prompt, isUseLargeGPT=True):
    """
    Использует разные апишки разных сеток.
        * isUseLargeGPT=True (по умолчанию)
            сетка   rugpt3large

            инфа    https://huggingface.co/sberbank-ai/rugpt3large_based_on_gpt2
        * isUseLargeGPT=False
            сетка   rugpt3small

            инфа    https://huggingface.co/sberbank-ai/rugpt3small_based_on_gpt2

    :param text:
    :return:
    """
    if isUseLargeGPT:
        link = __req_link_large
    else:
        link = __req_link_small

    body = __req_body(prompt=prompt)
    r = requests.post(link, json=body, headers=__req_headers)

    if r.status_code == 200:
        responseJson = json.loads(r.content.decode('utf-8'))
        return responseJson[0]['generated_text']
    else:
        import sys
        sys.stderr.write("asd")
        print("Ошибка запроса по адресу: " + r.request.url + ". Тело: " + body.__str__())
        print("")
        return "Ошибка " + r.status_code.__str__()
