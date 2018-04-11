from enum import Enum


class MessageType(Enum):
    TEXT = 'TEXT'
    DRAG = 'DRAG'
    CHECK_IDLENESS = 'CHECK_IDLENESS'
    CHECK_DS = 'CHECK_DS'
    USER_CONNECT = 'USER_CONNECT'
    USER_DISCONNECT = 'USER_DISCONNECT'


class MessageInfo:
    def __init__(self, msg_tag, msg_type, room_id, user_id, timestamp):
        self.msg_tag = msg_tag
        self.msg_type = msg_type
        self.room_id = room_id
        self.user_id = user_id
        self.timestamp = timestamp
