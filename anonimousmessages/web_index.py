#import telebot
from anonimousmessages.anonimBotYDB import RoomsYDBDatabase
import json

db = RoomsYDBDatabase()


def handler(bot, event):
    message = event['body']
    dd = json.loads(message)
    #bot.send_message(1265270129, str(dd))
    #bot.send_message(1265270129, str(dd.keys()))
    #bot.send_message(1265270129, dd['roomName'])
    try:
        #bot.send_message(1265270129, dd['roomName'])
        #bot.send_message(1265270129, str(db.get_room(dd['roomName'])))
        rooms = db.get_room(dd['roomName'])
        if len(rooms) == 0:
            bot.send_message(1265270129, str(dd))
        user_id = rooms[0]['user_id']
        bot.send_message(user_id, str(dd['message']))
    except Exception as e:
        bot.send_message(1265270129, str(e))



    #bot.send_message(1265270129, event['isBase64Encoded'])
    #bot.send_message(1265270129, event['headers'])
    #bot.send_message(1265270129, str(event['headers'].keys()))
    #bot.send_message(1265270129, str(event['headers']['dick']))






