from critical_moment import CriticalMoment
from message_tag import MessageTag
from alerter import alerter_util as au

MSG_TIME_INTERVAL_IN_SEC = 180
MIN_NUM_OF_TEC_MSGS_PER_GROUP = 5
MIN_NUM_OF_TEC_MSGS_PER_USER = 3


class TECAlerter:
    def __init__(self):
        self.message_info_by_room_id = {}  # <room_id, msg_info>
        self.tec_msg_by_user_in_room = {}  # <room_id, <user_id, msg_info>>

    def handle_message_tag(self, msg_info):
        if msg_info.room_id not in self.message_info_by_room_id.keys():
            self.message_info_by_room_id[msg_info.room_id] = []
        self.update_message_info_by_room_id(msg_info)

        if msg_info.room_id not in self.tec_msg_by_user_in_room.keys():
            self.tec_msg_by_user_in_room[msg_info.room_id] = {}
        if msg_info.user_id not in self.tec_msg_by_user_in_room[msg_info.room_id].keys():
            self.tec_msg_by_user_in_room[msg_info.room_id][msg_info.user_id] = []
        self.update_message_info_by_user_id(msg_info)

        if self.is_group_tec_alert(msg_info.room_id) or self.is_user_tec_alert(msg_info):
            return CriticalMoment.TEC

        return CriticalMoment.NONE

    def update_message_info_by_room_id(self, msg_info):
        self.message_info_by_room_id[msg_info.room_id] = \
            au.update_message_info_list_by_time_interval(self.message_info_by_room_id[msg_info.room_id],
                                                         msg_info, MSG_TIME_INTERVAL_IN_SEC)

    def update_message_info_by_user_id(self, msg_info):
        self.tec_msg_by_user_in_room[msg_info.room_id][msg_info.user_id] = \
            au.update_message_info_list_by_time_interval(
                self.tec_msg_by_user_in_room[msg_info.room_id][msg_info.user_id], msg_info, MSG_TIME_INTERVAL_IN_SEC)

    def is_group_tec_alert(self, room_id):
        return self.count_tec_msgs(self.message_info_by_room_id[room_id]) >= MIN_NUM_OF_TEC_MSGS_PER_GROUP

    def is_user_tec_alert(self, msg_info):
        return self.count_tec_msgs(self.tec_msg_by_user_in_room[msg_info.room_id][msg_info.user_id]) \
               >= MIN_NUM_OF_TEC_MSGS_PER_USER

    def count_tec_msgs(self, all_msgs):
        count_tec_msgs = 0
        for curr_msg_info in all_msgs:
            if curr_msg_info.msg_tag is MessageTag.TEC:
                count_tec_msgs += 1

        return count_tec_msgs
