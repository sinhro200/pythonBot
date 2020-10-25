import vk_api
import  requests
import  random
import  json
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
def uploadImages(images,offset,vk_session):
    session = requests.Session()
    attachments = []
    i=0;
    upload =vk_api.VkUpload(vk_session)
    while (i < 10 and i + offset < len(images)):
        image_url = images[i+offset]
        image = session.get(image_url, stream=True)
        photo = upload.photo_messages(photos=image.raw)[0]
        attachments.append(
            'photo{}_{}_{}'.format(photo['owner_id'], photo['id'],photo['access_key'])
         )
        i+=1
    return attachments
def getName (id):
    payload = {'user_id':id,'access_token':token,'v':'5.124'}
    response = requests.get("https://api.vk.com/method/users.get",params=payload)

    resp_keys = response.text.split(":")
    print(resp_keys)
    first_name = resp_keys[3]
    first_name=first_name.split(",")[0]
    first_name=first_name[1:]
    first_name = first_name[:-1]
    last_name = resp_keys[4]
    last_name = last_name.split(",")[0]
    last_name = last_name[1:]
    last_name = last_name[:-1]
    print(first_name)
    print(last_name)
    return  first_name +" "+ last_name
def getAll():
    message="Призываю вас:\n"
    for person in pivniye:
        message+=getLink(person)
    return  message
def getLink(id):
    id=str(id)
    return "[id"+id+"|"+getName(id)+"] \n"
def getPivniye():
    ids="\n"
    ids_set = set(pivniye)
    for id in ids_set:
        ids+=getName(id)
    return ids
def getPollInfo():
    info="\n"
    for time in poll.keys() :
            print(time)
            info +=time +"\n"
            for id in poll.get(time):
                info+=getName(id)
    return info
def whoIs(message,members):
    index = random.randrange(0,len(members))
    if str(members[index]["member_id"]) == "-"+group_id:
        if index == 0:
            index+=1
        elif index==len(members)-1:
            index-=1
    return  "Очевидно что "+message + " " +getName(members[index]["member_id"])

def addPollValue(value,id):
    ids=[]
    if value in poll.keys():
        ids=poll.get(value)
        if id in ids:
            return
    ids.append(id);
    poll.update({value:ids})
def createPollMessage(time_from,time_to):
    i = time_from
    poll_data="Варианты времени:\n"
    time_data=""
    while (i<= time_to):
        if(int(i)!=i):
            time_data=str(int(i))+":30"
        else:
            time_data=str(int(i))+":00"
        time_values.append(time_data)
        poll_data+=time_data+"\n"
        i+=0.5
    return poll_data


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


# API-ключ созданный ранее
token = "5053247a0cad934c798750243f5425b84ae062a99be994dce2194b7255b8d2afa066a91769e352f2a8f8c"

# Авторизуемся как сообщество
vk_session = vk_api.VkApi(token=token, api_version='5.124')
group_id="199735512"
# Работа с сообщениями
longpoll = VkBotLongPoll(vk_session,group_id)
vk = vk_session.get_api()

pivniye = []
poll_created= 0
poll= {};
time_values=[]
# Основной цикл
for event in longpoll.listen():
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat and "пивобот " in str(event):
            random_id = random.randrange(10000,90000)
            chat_id = int(event.chat_id)
            print(event.message)
            if "пиво попито" in str(event):
                pivniye = []
                poll_created = 0
                poll = {};
                time_values = []
                vk.messages.send(
                    random_id=random_id,
                    chat_id=chat_id,
                    message="Везет)",
                )
            if "общий сбор" in str(event):
                vk.messages.send(
                    random_id=random_id,
                    chat_id=chat_id,
                    message=getAll(),
                )

            if "иду" in str(event):
                 if str(event.message.from_id) not in pivniye:
                     pivniye.append(str(event.message.from_id))
                     message = "Принял"
                 else:
                     message= "Я уже понял"
                 vk.messages.send(
                     random_id=random_id,
                     chat_id=chat_id,
                     message=message,
                 )
            if "кто идет" in str(event):
                message = "Идут пить пиво :" + getPivniye()
                vk.messages.send(
                    random_id=random_id,
                    chat_id=chat_id,
                    message=message,
                )
                continue
            if "кто" in str(event):
                members = vk.messages.getConversationMembers(peer_id=2000000000 +event.chat_id, v=5.124,group_id=group_id)["items"]
                message = whoIs(event.message.text[11:], members)
                vk.messages.send(
                    random_id=random_id,
                    chat_id=chat_id,
                    message=message,
                )
            if "опрос время" in str(event):
                time="empty"
                try:
                    times= str(event.message.text).split("опрос время ")[1]
                    times=times.split(" ")
                    if int(times[0])>int(times[1]):
                        vk.messages.send(
                            random_id=random_id,
                            chat_id=chat_id,
                            message="Ты че дурак чтоли а",
                        )
                        continue
                    poll_message=createPollMessage(int(times[0]),int(times[1]))
                    poll_created=1
                except BaseException  :
                    poll_message= "Неверно задано время"
                print(time_values)
                vk.messages.send(
                  random_id=random_id,
                  chat_id=chat_id,
                  message=poll_message,
                )
            if "я за" in str(event):
                if not poll_created :
                    message = "Нет опроса"
                else:
                    time="empty"
                    try:
                        time= str(event.message.text).split("я за ")[1]
                        print(time)
                        if not time in time_values:
                            message = "Время не в диапазоне соси"
                        else:
                            addPollValue(time,event.message.from_id)
                            message = "Принял"
                    except BaseException  :
                        message= "Неверно задано время"
                print(poll)
                vk.messages.send(
                    random_id=random_id,
                    chat_id=chat_id,
                    message=message,
                )
            if "время инфо" in str(event):
                if not poll_created :
                    message = "Нет опроса"
                else:
                    message=getPollInfo()
                vk.messages.send(
                    random_id=random_id,
                    chat_id=chat_id,
                    message=message,
                )
            if "лучшее пиво" in str(event):
                vk.messages.send(
                    random_id=random_id,
                    chat_id=chat_id,
                    message="Конечно же ипа",
                )
            if "команды" in str(event):
                message = "Команды бота: \n " \
                              "пивобот иду - готов идти пить пиво \n  " \
                              "пивобот кто идет - посмотреть кто готов идти пить пиво \n" \
                              "пивобот опрос время #время_от #время_до - опрос по времени в интервале \n " \
                              "пивобот я за #время - проголосовать за данное время в опросе \n" \
                              "пивобот скидка #[пятерочка/магнит/кб] - показать акции данного магазина\n" \
                              "пивобот время инфо - показать результаты опроса по времени\n" \
                              "пивобот лучшее пиво - показать лучшее пиво во вселенной\n"\
                              "пивобот кто #текст - ну вы поняли\n"\

                vk.messages.send(
                    random_id=random_id,
                    chat_id=chat_id,
                    message=message,
                )
            if "скидка" in str(event):
                message=''
                if("пятерочка" in str(event)):
                    images = parsePyaterochka()
                    message="Скидки в пятерочке"
                elif("магнит" in str(event)):
                    images = parseMagnit()
                    message = "Скидки в магните "
                elif ("кб" in str(event)):
                    products= parseKb()
                    message="Скидки в кб: \n"
                    for product in products.keys():
                        message+=product + " : " +products[product] +"р \n"
                    vk.messages.send(
                        random_id=random_id ,
                        chat_id=chat_id,
                        message=message,
                    )
                    continue
                else:
                    vk.messages.send(
                        random_id=random_id + i,
                        chat_id=chat_id,
                        message="Я не знаю такого магазина",
                    )
                    continue
                length = len(images)
                i=0;
                while True:
                    attachments= uploadImages(images,i,vk)
                    vk.messages.send(
                        random_id=random_id+i,
                        chat_id=chat_id,
                        message=message,
                        attachment=','.join(attachments)
                    )
                    i+=10
                    if(i>length):
                        break

