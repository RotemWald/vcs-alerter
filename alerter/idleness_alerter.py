from critical_moment import CriticalMoment
from message_info import MessageType
from alerter import alerter_util as au

IDLE_MSG_TIME_INTERVAL_IN_SEC_BY_ROOM = 180
IDLE_TIME_INTERVAL_IN_SEC_BY_USER = 300
IDLE_DRAG_TIME_INTERVAL_IN_SEC_BY_ROOM = 420
TIME_BEFORE_FIRST_ALERT_IN_SECONDS = 300


class IdlenessAlerter:
    def __init__(self):
        self.last_message_by_room_id = {}  # <room_id, timestamp>
        self.last_drag_by_room_id = {}  # <room_id, timestamp>
        self.last_message_or_drag_by_user_in_room = {}  # <room_id, <user_id, timestamp>>
        self.first_msg_timestamp_by_room_id = {}  # <room_id, timestamp>

    def handle_message_tag(self, msg_info):
        if msg_info.room_id not in self.last_message_or_drag_by_user_in_room.keys():
            self.last_message_or_drag_by_user_in_room[msg_info.room_id] = {}

        # initiate dictionaries for first message
        if msg_info.room_id not in self.last_message_by_room_id.keys()\
                and (msg_info.msg_type is MessageType.TEXT or msg_info.msg_type is MessageType.DRAG):
            self.last_message_by_room_id[msg_info.room_id] = msg_info.timestamp
            self.last_drag_by_room_id[msg_info.room_id] = msg_info.timestamp
            self.first_msg_timestamp_by_room_id[msg_info.room_id] = msg_info.timestamp
            self.update_last_message_or_drag_by_users_in_groups(msg_info)

        if msg_info.msg_type is MessageType.TEXT:
            self.last_message_by_room_id[msg_info.room_id] = msg_info.timestamp
        elif msg_info.msg_type is MessageType.DRAG:
            self.last_drag_by_room_id[msg_info.room_id] = msg_info.timestamp

        if msg_info.msg_type is MessageType.USER_CONNECT:
            self.update_user_connect(msg_info)
            return

        if msg_info.msg_type is MessageType.USER_DISCONNECT:
            self.update_user_disconnect(msg_info)
            return

        self.last_message_or_drag_by_user_in_room[msg_info.room_id][msg_info.user_id] = msg_info.timestamp

    def check_idleness(self, timestamp):
        idle_room_ids = []
        for room_id in self.last_message_by_room_id.keys():
            if self.check_idleness_in_specific_room(room_id, timestamp) is CriticalMoment.IDLENESS:
                idle_room_ids.append(room_id)

        return idle_room_ids

    def check_idleness_in_specific_room(self, room_id, timestamp):
        if (not self.is_room_open(room_id))\
                or au.in_time_interval(self.first_msg_timestamp_by_room_id[room_id], timestamp,
                                       TIME_BEFORE_FIRST_ALERT_IN_SECONDS):
            return CriticalMoment.NONE

        # rule 1
        if au.out_time_interval(self.last_message_by_room_id[room_id], timestamp, IDLE_MSG_TIME_INTERVAL_IN_SEC_BY_ROOM)\
                and au.out_time_interval(self.last_drag_by_room_id[room_id], timestamp,
                                         IDLE_MSG_TIME_INTERVAL_IN_SEC_BY_ROOM):
            return CriticalMoment.IDLENESS

        # rule 2
        if au.out_time_interval(self.last_drag_by_room_id[room_id], timestamp,
                                IDLE_DRAG_TIME_INTERVAL_IN_SEC_BY_ROOM):
            return CriticalMoment.IDLENESS

        # rule 3
        for user_id in self.last_message_or_drag_by_user_in_room[room_id].keys():
            if au.out_time_interval(self.last_message_or_drag_by_user_in_room[room_id][user_id],
                                    timestamp, IDLE_TIME_INTERVAL_IN_SEC_BY_USER):
                return CriticalMoment.IDLENESS

        return CriticalMoment.NONE

    def update_user_connect(self, msg_info):
        self.last_message_or_drag_by_user_in_room[msg_info.room_id][msg_info.user_id] = msg_info.timestamp

    def update_user_disconnect(self, msg_info):
        if msg_info.user_id in self.last_message_or_drag_by_user_in_room[msg_info.room_id]:
            del self.last_message_or_drag_by_user_in_room[msg_info.room_id][msg_info.user_id]
        if len(self.last_message_or_drag_by_user_in_room[msg_info.room_id].keys()) is 0:
            del self.last_message_or_drag_by_user_in_room[msg_info.room_id]
            del self.last_message_by_room_id[msg_info.room_id]
            del self.last_drag_by_room_id[msg_info.room_id]
            del self.first_msg_timestamp_by_room_id[msg_info.room_id]

    def is_room_open(self, room_id):
        # check that the room is open and that the number of users is bigger than zero
        return room_id in self.first_msg_timestamp_by_room_id.keys()\
               and len(self.last_message_or_drag_by_user_in_room[room_id].keys()) > 0

    def update_last_message_or_drag_by_users_in_groups(self, msg_info):
        for user_id in self.last_message_or_drag_by_user_in_room[msg_info.room_id].keys():
            self.last_message_or_drag_by_user_in_room[msg_info.room_id][user_id] = msg_info.timestamp
