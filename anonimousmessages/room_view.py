
base_address = "https://anonmessage.na4u.ru/"


class RoomView:
    def __init__(self, rooms_or_room):
        self.rooms_list = []
        if type(rooms_or_room) is list:
            for room in rooms_or_room:
                self.rooms_list.append(OneRoomView(room))
        else:
            self.rooms_list.append(OneRoomView(rooms_or_room))

    def __str__(self):
        return "\n\n".join((str(room) for room in self.rooms_list))


class OneRoomView:
    def __init__(self, room):
        self.user_id = room["user_id"]
        self.room_name = room["room_name"]
        self.is_public = room["is_public"] == "1"
        self.password = room["password"]

    def __str__(self):
        if self.is_public:
            return f"владелец: {self.user_id}, доступна по адресу {base_address}{self.room_name}"
        else:
            return f"владелец: {self.user_id}, доступна по адресу {base_address}{self.room_name}" \
                   f"\n\t пароль: {self.password}"
