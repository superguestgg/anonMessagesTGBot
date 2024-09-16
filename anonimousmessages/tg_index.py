import random
from functools import cache
import sys

# sys.path.insert(2, '.')
# from anonimBotYDB import RoomsYDBDatabase
from anonimousmessages.anonimBotYDB import RoomsYDBDatabase
from anonimousmessages.room_view import RoomView


# def set_up():
#    global db
#    db = RoomsYDBDatabase()


# @cache
# def lazy_set_up():
#    print("AnonimMessage lazy_set_up")
#    set_up()


class AnonimMessage:
    def __init__(self, bot):
        self.bot = bot
        self.db = RoomsYDBDatabase()

    def set_up(self):
        self.bot.message_handler(commands=['rooms_commands'])(self.rooms_send_commands_help)
        self.bot.message_handler(commands=['rooms_help'])(self.rooms_help)
        self.bot.message_handler(commands=['my_rooms'])(self.my_rooms)
        self.bot.message_handler(commands=['all_rooms'])(self.all_rooms)
        self.bot.message_handler(commands=['get_room'])(self.get_room)
        self.bot.message_handler(commands=['create_public_room'])(self.create_public_room)
        self.bot.message_handler(commands=['create_private_room'])(self.create_private_room)
        self.bot.message_handler(commands=['delete_room'])(self.delete_room)
        # self.db.delete_table()
        # self.db.set_up()

    def create_room(self, author, room_name, is_public=True, password=""):
        pass

    def rooms_send_commands_help(self, message):
        print(self)
        self.bot.reply_to(message, '/rooms_help информация'
                                   '\n/rooms_commands это меню с командами'
                                   '\n/get_room моя публичная комната'
                                   '\n/my_rooms показать список моих комнат'
                                   '\n/all_rooms показать список всех комнат'
                                   '\n/create_public_room создать публичную комнату'
                                   '\n/create_private_room <password> создать приватную комнату с паролем'
                                   '\n/delete_room <room_name> удалить комнату по имени')

    def rooms_help(self, message):
        self.bot.send_message(message.chat.id, 'Это новый пакет в моем боте,'
                                               ' здесь вы можете создать комнаты'
                                               ' с публичным адресом на сайте в интернете,'
                                               ' через ккоторый можно писать вам сообщения'
                                               '\n/rooms_commands меню с командами')

    def my_rooms(self, message):
        rooms = self.db.get_rooms_by_user(message.from_user.id)
        # rooms = self.db.read_all_rooms()
        self.bot.send_message(message.chat.id, 'Ваши комнаты:\n'
                                               f'{RoomView(rooms)}')

    def all_rooms(self, message):
        if message.from_user.id == 1265270129:
            self.bot.send_message(message.chat.id, 'Недостаточно прав')
        rooms = self.db.read_all_rooms()
        self.bot.send_message(message.chat.id, 'Все комнаты:\n'
                                               f'{RoomView(rooms)}')

    def get_room(self, message):
        rooms = self.db.get_room(message.from_user.username)
        self.bot.send_message(message.chat.id, 'Ваша публичная комната:\n'
                                               f'{RoomView(rooms)}')

    def create_public_room(self, message):
        room_name = message.from_user.username
        self.db.create_room(message.from_user.id, room_name)
        room = self.db.get_room(room_name)
        self.bot.send_message(message.chat.id, f'Комната {room_name} создана, вот она:\n'
                                               f'{RoomView(room)}')

    def create_private_room(self, message):
        password = message.text.replace("/create_private_room ", "")
        room_name = str(random.random()).replace(".", "")
        self.db.create_room(message.from_user.id, room_name, False, password)
        room = self.db.get_room(room_name)
        self.bot.send_message(message.chat.id, f'Комната {room_name} создана, вот она:\n'
                                               f'{RoomView(room)}')

    def delete_room(self, message):
        room_name = message.text.replace("/delete_room ", "")
        user_id = message.from_user.id
        self.db.delete_room(user_id, room_name)
        self.bot.send_message(message.chat.id, f'room {message.text.replace("/delete_room ", "")} has beed deleted')
