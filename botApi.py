import random
import requests
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import bdApi
from pivoParser import parsePyaterochka, parseMagnit, parseKb
from pivoParserSelenium import *


def uploadImages(images, offset, vk_session):
    session = requests.Session()
    attachments = []
    i = 0
    upload = vk_api.VkUpload(vk_session)
    while i < 10 and i + offset < len(images):
        image_url = images[i + offset]
        image = session.get(image_url, stream=True)
        photo = upload.photo_messages(photos=image.raw)[0]
        attachments.append(
            'photo{}_{}_{}'.format(photo['owner_id'], photo['id'], photo['access_key'])
        )
        i += 1
    return attachments


def getRandomBeerMessage(vk_session):
    beer = randomBeerParser()
    msg = "Почему бы сегодня не выпить: \n"
    msg += "🍺" + beer['name'] + '\n' + "⭐" + beer['rating'] + "\n 💬Отзывы:\n" + beer['url']
    image_url = beer['image']
    session = requests.Session()
    upload = vk_api.VkUpload(vk_session)
    image = session.get(image_url, stream=True)
    photo = upload.photo_messages(photos=image.raw)[0]
    attachments = 'photo{}_{}_{}'.format(photo['owner_id'], photo['id'], photo['access_key'])
    vk.messages.send(
        random_id=random_id,
        chat_id=chat_id,
        message=msg,
        attachment=attachments
    )


def getName(id):
    payload = {'user_id': id, 'access_token': token, 'v': '5.124', 'lang': 1}
    response = requests.get("https://api.vk.com/method/users.get", params=payload)
    print(response)
    resp_keys = response.text.split(":")
    print(resp_keys)
    first_name = resp_keys[2]
    first_name = first_name.split(",")[0]
    first_name = first_name[1:]
    first_name = first_name[:-1]
    last_name = resp_keys[4]
    last_name = last_name.split(",")[0]
    last_name = last_name[1:]
    last_name = last_name[:-1]
    print(first_name)
    print(last_name)
    return first_name + " " + last_name


def getAll(current_chat_id):
    message = "Призываю вас:\n"
    ids = []
    poll = bdApi.getPollByChatId(current_chat_id)
    if poll is None or poll == "NULL":
        return message
    for array in poll.values():
        if array is not None:
            for id in array:
                ids.append(id)
    ids = set(ids)
    for id in ids:
        message += "🧍" + getLink(id) + "\n"
    return message


def getLink(id):
    id = str(id)
    return "[id" + id + "|" + getName(id) + "] \n"


def getFavourites(user_id):
    msg = "Ваше избранное пиво: \n"
    array = bdApi.getUsersFavourites(user_id)
    if array is None:
        return msg
    for element in array:
        print(element)
        msg += "&#12288;⭐" + element + "\n"
    return msg


def byShopSort(t):
    return t['market']


def getFavouritesDiscounts(user_id):
    msg = "Скидки на ваше избранное пиво:\n"
    array = bdApi.getUsersFavourites(user_id)
    if array is None:
        return msg
    for element in array:
        msg += "\n⭐" + element + ":"
        discounts = byProductEdadealParser(element)
        discounts.sort(key=byShopSort)
        for disount in discounts:
            msg += "\n&#12288;🍺🍺" + disount['description'] + "\n " + "&#12288;🛒🛒" + disount[
                'market'] + "\n" + "&#12288;💲💲" + disount['priceNew'] + "\n"
    return msg


def removeFromFavourites(user_id, fav_name):
    msg = "Удалено: " + fav_name
    array = bdApi.getUsersFavourites(user_id)
    if array is None:
        return "Список пуст"
    array = list(array)
    try:
        array.remove(name)
    except ValueError:
        return "Нет такого пива в спике"
    bdApi.updateUsersFavourites(user_id, array)
    return msg


def getPivniye(current_chat_id):
    ids = "\n"
    poll = bdApi.getPollByChatId(current_chat_id)
    if poll == "NULL" or poll is None:
        ids += "Никто\n"
        return ids
    ids_set = set()
    for element in poll.values():
        if element is not None:
            ids_set.update(set(element))
    print(ids_set)
    for id in ids_set:
        ids += "&#12288;🧍" + getName(id) + "\n"
    return ids


def getPollInfo(current_chat_id):
    info = "Инфо по голосам: \n"
    poll = bdApi.getPollByChatId(current_chat_id)
    if poll is None or poll == "NULL":
        return "Нет опроса"
    for time in poll.keys():
        if poll.get(time) is not None:
            info += "⏱" + time + ": \n"
            for id in poll.get(time):
                info += "&#12288;🧍" + getName(id) + '\n'
            info += "\n"
    return info


def whoIs(message, members):
    index = random.randrange(0, len(members) - 1)
    while members[index]["member_id"] < 0:
        index = random.randrange(0, len(members) - 1)
    return "🤔Очевидно что " + message + " " + getName(members[index]["member_id"])


def addPollValue(value, id, current_chat_id):
    ids = []
    poll = bdApi.getPollByChatId(current_chat_id)
    if value in poll.keys():
        ids = poll.get(value)
        if ids == None:
            ids = []
        if id in ids:
            return
    ids.append(id)
    poll.update({value: ids})
    bdApi.updatePoll(current_chat_id, poll)


def createPollMessage(time_from, time_to, current_chat_id):
    i = time_from
    poll_data = "Варианты времени:\n"
    time_data = ""
    time_values = []
    while i <= time_to:
        if int(i) != i:
            time_data = str(int(i)) + ":30"
        else:
            time_data = str(int(i)) + ":00"
        time_values.append(time_data)
        poll_data += time_data + "\n"
        i += 0.5
    time_values.append("Не важно")
    bdApi.updatePoll(current_chat_id, {key: None for key in time_values})
    return poll_data


def getVoteKeyboard(current_chat_id):
    settings = dict(one_time=False, inline=True)
    keyboard = VkKeyboard(**settings)
    poll = bdApi.getPollByChatId(current_chat_id)
    if poll is None or poll == "NULL":
        return None
    i = 0
    for time_value in poll.keys():
        i += 1
        print("time value" + str(time_value))
        keyboard.add_callback_button(label="я за " +time_value, color=VkKeyboardColor.POSITIVE)
        if i % 3 == 0:
            keyboard.add_line()
    keyboard.add_callback_button(label='голоса инфо', color=VkKeyboardColor.SECONDARY)
    keyboard.add_callback_button(label='кто идет', color=VkKeyboardColor.SECONDARY)

    return keyboard


# API-ключ созданный ранее
token = os.environ.get('ACCESS_TOKEN')
# Авторизуемся как сообщество
vk_session = vk_api.VkApi(token=token, api_version='5.124')
group_id = os.environ.get('GROUP_ID')
# Работа с сообщениями
longpoll = VkBotLongPoll(vk_session, group_id)
vk = vk_session.get_api()


def showPoll(current_chat_id, poll_keyboard):
    poll = bdApi.getPollByChatId(current_chat_id)
    if poll is None or poll_keyboard is None:
        vk.messages.send(
            random_id=random_id,
            chat_id=current_chat_id,
            message="Нет опроса")
    else:
        vk.messages.send(
            random_id=random_id,
            chat_id=current_chat_id,
            message="Текущий опрос",
            keyboard=poll_keyboard.get_keyboard()
        )


def showVoteInfoInDetails(current_chat_id):
    msg: str
    poll = bdApi.getPollByChatId(current_chat_id)
    if poll is None or poll == "NULL":
        msg = "Нет опроса"
    else:
        msg = getPollInfo(current_chat_id)
    vk.messages.send(
        random_id=random_id,
        chat_id=current_chat_id,
        message=msg,
    )


def getPivoDrinkers(current_chat_id):
    msg = "Идут пить пиво :" + getPivniye(current_chat_id)
    vk.messages.send(
        random_id=random_id,
        chat_id=current_chat_id,
        message=msg,
    )


def addFavourite(user_id, fav_name):
    names = bdApi.getUsersFavourites(user_id)
    if names is None:
        names = []
    names.append('"' + fav_name + '"')
    bdApi.updateUsersFavourites(user_id, names)


def handleVote(current_chat_id):
    msg: str
    poll = bdApi.getPollByChatId(current_chat_id)
    if poll is None:
        msg = "Нет опроса"
    else:
        time = "empty"
        try:
            cur_time = str(event.message.text[33:])
            if cur_time not in poll.keys():
                msg = "Время не в диапазоне соси"
            else:
                addPollValue(cur_time, event.message.from_id, chat_id)
                msg = "Принял"
        except BaseException:
            msg = "Неверно задано время"
    print(poll)
    vk.messages.send(
        random_id=random_id,
        chat_id=current_chat_id,
        message=msg,
    )


# Основной цикл
# FIXME [ZK]: пивобот does not follows exact order of commands
for event in longpoll.listen():
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat and ("@public" + group_id) in str(event):
            poll = bdApi.getPollByChatId(chat_id)
            if poll is not None and str(event.message.text[33:]) in poll.keys():
                handleVote(chat_id)
                continue
            if "голоса инфо" in str(event):
                showVoteInfoInDetails(chat_id)
                continue
            if "кто идет" in str(event):
                getPivoDrinkers(chat_id)
                continue

        if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat and (
                "пивобот " in str(event) or "Пивобот " in str(event)) and (event.message.text[1:7] == "ивобот"):
            random_id = random.randrange(10000, 90000)
            chat_id = int(event.chat_id)
            if "опрос показать" in str(event):
                keyboard = getVoteKeyboard(chat_id)
                if keyboard is None:
                    vk.messages.send(
                        random_id=random_id,
                        chat_id=chat_id,
                        message="Нет опроса",
                    )
                    continue
                showPoll(chat_id, keyboard)
                continue
            if "пиво попито" in str(event):
                bdApi.cleanPoll(chat_id)
                vk.messages.send(
                    random_id=random_id,
                    chat_id=chat_id,
                    message="Везет)",
                )
            if "добавить в избранное" in str(event):
                name = event.message.text[29::]
                addFavourite(event.message.from_id, name)
                vk.messages.send(
                    random_id=random_id,
                    chat_id=chat_id,
                    message="добавлено в избранное",
                )
            if "показать избранное" in str(event):
                message = getFavourites(event.message.from_id)
                vk.messages.send(
                    random_id=random_id,
                    chat_id=chat_id,
                    message=message,
                )
            if "скидки на избранное" in str(event):
                message = getFavouritesDiscounts(event.message.from_id)
                vk.messages.send(
                    random_id=random_id,
                    chat_id=chat_id,
                    message=message,
                )
            if "удалить из избранного" in str(event):
                name = event.message.text[30::]
                print(name)
                message = removeFromFavourites(event.message.from_id, name)
                vk.messages.send(
                    random_id=random_id,
                    chat_id=chat_id,
                    message=message,
                )
            if "общий сбор" in str(event):
                vk.messages.send(
                    random_id=random_id,
                    chat_id=chat_id,
                    message=getAll(chat_id),
                )
            if "случайное пиво" in str(event):
                getRandomBeerMessage(vk)
                continue

            if "кто идет" in str(event):
                getPivoDrinkers(chat_id)
                continue
            if "кто" in str(event):
                members = \
                    vk.messages.getConversationMembers(peer_id=2000000000 + event.chat_id, v=5.124, group_id=group_id)[
                        "items"]
                message = whoIs(event.message.text[11:], members)
                vk.messages.send(
                    random_id=random_id,
                    chat_id=chat_id,
                    message=message,
                )
            if 'опрос время' in str(event):
                time = "empty"
                try:
                    times = str(event.message.text).split("опрос время ")[1]
                    times = times.split(" ")
                    print(times)
                    if int(times[0]) > int(times[1]) or int(times[1]) - int(times[0]) > 4:
                        vk.messages.send(
                            random_id=random_id,
                            chat_id=chat_id,
                            message="Ты че дурак чтоли а",
                        )
                        continue
                    createPollMessage(int(times[0]), int(times[1]), chat_id)
                    keyboard = getVoteKeyboard(chat_id)
                    showPoll(chat_id, keyboard)
                    continue
                except BaseException:
                    vk.messages.send(
                        random_id=random_id,
                        chat_id=chat_id,
                        message="Неверно задано время",
                    )

            if "голоса инфо" in str(event):
                showVoteInfoInDetails(chat_id)
                continue
            if "лучшее пиво" in str(event):
                vk.messages.send(
                    random_id=random_id,
                    chat_id=chat_id,
                    message="Конечно же ипа",
                )
            if "команды" in str(event):
                message = ("Команды бота: \n"
                           "🍻пивобот кто идет - посмотреть кто готов идти пить пиво \n"
                           "🍻пивобот опрос время #время_от #время_до - опрос по времени, разница не более 4 часов\n"
                           "🍻пивобот опрос показать - выводит опрос\n"
                           "🍻пивобот скидкаонлайн #[пятерочка/магнит/кб] - акции магазина со skidkaonline\n"
                           "🍻пивобот едадил #[пятерочка/магнит/кб] - акции магазина с едадила\n"
                           "🍻пивобот голоса инфо - показать результаты опроса по времени\n"
                           "🍻пивобот лучшее пиво - показать лучшее пиво во вселенной\n"
                           "🍻пивобот кто #текст - ну вы поняли\n"
                           "🍻пивобот добавить в избранное #название - добавить пиво в избранное\n"
                           "🍻пивобот удалить из избранного #навзание - убрать из избранного\n"
                           "🍻пивобот показать избранное - показать ваше избранное пиво\n"
                           "🍻пивобот скидки на избранное - скидки на ваше избранное пиво\n"
                           "🍻пивобот случайное пиво - посоветовать случайное пиво\n")

                vk.messages.send(
                    random_id=random_id,
                    chat_id=chat_id,
                    message=message,
                )
            if "едадил" in str(event):
                message = ''
                if "пятерочка" in str(event):
                    products = edadeal_parser("5ka")
                    message = "Скидки в пятерочке: \n"
                elif "магнит" in str(event):
                    products = edadeal_parser("magnit-univer")
                    message = "Скидки в магните: \n "
                elif "кб" in str(event):
                    products = edadeal_parser("krasnoeibeloe")
                    message = "Скидки в кб: \n"
                else:
                    vk.messages.send(
                        random_id=random_id,
                        chat_id=chat_id,
                        message="Не знаю такого магазина",
                    )
                    continue
                for product in products:
                    message += product['description'] + " \n " + product['priceNew'] + "\n "
                vk.messages.send(
                    random_id=random_id,
                    chat_id=chat_id,
                    message=message,
                )

            if "скидкаонлайн" in str(event):
                message = ''
                if "пятерочка" in str(event):
                    images = parsePyaterochka()
                    message = "Скидки в пятерочке"
                elif "магнит" in str(event):
                    images = parseMagnit()
                    message = "Скидки в магните "
                elif "кб" in str(event):
                    products = parseKb()
                    message = "Скидки в кб: \n"
                    for product in products.keys():
                        message += product + " : " + products[product] + "р \n"
                    vk.messages.send(
                        random_id=random_id,
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
                i = 0
                while True:
                    attachments = uploadImages(images, i, vk)
                    vk.messages.send(
                        random_id=random_id + i,
                        chat_id=chat_id,
                        message=message,
                        attachment=','.join(attachments)
                    )
                    i += 10
                    if i > length:
                        break
