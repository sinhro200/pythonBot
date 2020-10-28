import psycopg2
import json
import os




DB = str(os.environ.get('DATABASE_NAME'))
USER =str(os.environ.get('DATABASE_USERNAME'))
PASSWORD =str(os.environ.get('DATABASE_PASSWORD'))
HOST =str(os.environ.get('DATABASE_HOST'))
PORT = str(os.environ.get('DATABASE_PORT'))
conn = psycopg2.connect(dbname='{}'.format(DB),
                        user='{}'.format(USER),
                        password='{}'.format(PASSWORD),
                        host='{}'.format(HOST),
                        port='{}'.format(PORT)
                        )


def getPollByChatId(chat_id):
    cursor = conn.cursor()
    chat_id = str(chat_id)
    cursor.execute("select poll from chats where chat_id = %s", chat_id)
    json_poll = cursor.fetchall()
    if not json_poll:
        return None
    elif json_poll[0][0] is None:
        return "NULL"
    poll = json_poll[0][0]
    print(poll)
    return poll


def getUsersFavourites(chat_user_id):
    cursor = conn.cursor()
    chat_user_id = str(chat_user_id)
    print(chat_user_id)
    cursor.execute("select favourites from users where user_id = {}".format( chat_user_id))
    json_favs = cursor.fetchall()
    print(json_favs)
    if not json_favs:
        return None
    return json_favs[0][0]


def updateUsersFavourites(user_id, favourites):
    cursor = conn.cursor()
    user_id = str(user_id)
    cursor.execute("select favourites from users where user_id ={} ".format( user_id))
    json_favs = cursor.fetchall()
    favourites = '{' + ','.join(favourites) + '}'
    if not json_favs:
        cursor.execute("insert into users (user_id,favourites,city)values ({},'{}',NULL )".format (user_id, favourites))
    else:
        cursor.execute("update users set favourites= '{}' where user_id ={}".format (favourites, user_id))
    conn.commit()

def updateCity(user_id,city):
    cursor = conn.cursor()
    user_id = str(user_id)
    cursor.execute("select * from users where user_id ={} ".format(user_id))
    data = cursor.fetchall()
    if not data:
        favs="{}"
        cursor.execute("insert into users (user_id,favourites,city)values ({},'{}','{}')".format(user_id,favs, city))
    else:
        cursor.execute("update users set city= '{}' where user_id ={}".format(city, user_id))
    conn.commit()
def getCity(user_id):
    cursor = conn.cursor()
    user_id = str(user_id)
    cursor.execute("select city from users where user_id ={} ".format(user_id))
    city=cursor.fetchall()[0][0]
    if city is None:
        city="Воронеж"
    return (city)


def updatePoll(chat_id, poll):
    cursor = conn.cursor()
    chat_id = str(chat_id)

    if getPollByChatId(chat_id) is None:
        createPoll(chat_id, poll)
    else:
        json_poll = json.dumps(poll)
        cursor.execute("update  chats set poll = %s where chat_id = %s", (json_poll, chat_id))
        conn.commit()


def cleanPoll(chat_id):
    cursor = conn.cursor()
    chat_id = str(chat_id)
    cursor.execute("update  chats set poll = NULL where chat_id = %s", chat_id)
    conn.commit()


def createPoll(chat_id, poll):
    print("create")
    cursor = conn.cursor()
    chat_id = str(chat_id)
    json_poll = json.dumps(poll)
    cursor.execute("insert into chats(chat_id,poll) values(%s, %s)", (chat_id, json_poll))
    conn.commit()
