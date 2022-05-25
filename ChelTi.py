import requests
import vk_api
import requests
import time

access_token = '50b566fdfe8808e0b14b1751a82d14ed6a92862aff6e49693dc638886b3b2ab314ef6ca7a4d1980098b9c'

vk_session = vk_api.VkApi(login='89009590792', password='Iwakura1488228322', api_version='5.130')
vk_session.auth()
vk = vk_session.get_api()

vals = {'status': '232'}
value = 1000
req = requests.get('https://oauth.vk.com/authorize?client_id=7844193&display=page&scope=friends&response_type=token&v=5.130')
print(req.text)
while value > 0:
    url = 'https://api.vk.com/method/account.saveProfileInfo?status='+str(value) +\
          '&v=5.130&access_token=2779da4217246f3949d477cc5ec86c846f6ffe346d9506711058f3ffde203b39b69865847126f207db71c'
    resp = requests.get(url)
    print(resp.text)
    time.sleep(1)
    value=value-7

