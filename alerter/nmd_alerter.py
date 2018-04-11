from critical_moment import CriticalMoment
from message_tag import MessageTag
from alerter import alerter_util as au

NMD_PERCENT_TO_ALERT = 0.7
USER_NMD_MSGS_CRITERIA = 4
MSG_TIME_INTERVAL_IN_SEC = 180
MIN_NUM_MSG_IN_INTERVAL = 10
TIME_BEFORE_FIRST_ALERT_IN_SECONDS = 300


class NMDAlerter:
    def __init__(self):
        self.message_info_by_room_id = {}  # <room_id, msg_info>
        self.nmd_msg_counter_by_user_in_room = {}  # <room_id, <user_id, counter>>
        self.first_msg_timestamp_by_room_id = {}  # <room_id, timestamp>

    def handle_message_tag(self, msg_info):
        if msg_info.room_id not in self.message_info_by_room_id.keys():
            self.message_info_by_room_id[msg_info.room_id] = []
            self.first_msg_timestamp_by_room_id[msg_info.room_id] = msg_info.timestamp
        self.update_message_info_by_room_id(msg_info)

        if msg_info.room_id not in self.nmd_msg_counter_by_user_in_room.keys():
            self.nmd_msg_counter_by_user_in_room[msg_info.room_id] = {}
        if msg_info.user_id not in self.nmd_msg_counter_by_user_in_room[msg_info.room_id].keys():
            self.nmd_msg_counter_by_user_in_room[msg_info.room_id][msg_info.user_id] = 0

        if msg_info.msg_tag is MessageTag.NMD:
            self.nmd_msg_counter_by_user_in_room[msg_info.room_id][msg_info.user_id] += 1
        else:
            self.nmd_msg_counter_by_user_in_room[msg_info.room_id][msg_info.user_id] = 0

        # check if we should send NMD alert
        if (self.is_group_nmd_alert(msg_info.room_id) or self.is_user_nmd_alert(msg_info))\
                and (au.out_time_interval(self.first_msg_timestamp_by_room_id[msg_info.room_id], msg_info.timestamp,
                                          TIME_BEFORE_FIRST_ALERT_IN_SECONDS)):
            return CriticalMoment.NMD

        return CriticalMoment.NONE

    def update_message_info_by_room_id(self, msg_info):
        self.message_info_by_room_id[msg_info.room_id] = au.update_message_info_list_by_time_interval\
            (self.message_info_by_room_id[msg_info.room_id], msg_info, MSG_TIME_INTERVAL_IN_SEC)

    def is_group_nmd_alert(self, room_id):
        count_nmd_msgs = 0
        count_total_msgs = 0
        for msg_info in self.message_info_by_room_id[room_id]:
            count_total_msgs += 1
            if msg_info.msg_tag is MessageTag.NMD:
                count_nmd_msgs += 1

        return count_nmd_msgs / count_total_msgs >= NMD_PERCENT_TO_ALERT and count_total_msgs >= MIN_NUM_MSG_IN_INTERVAL

    def is_user_nmd_alert(self, msg_info):
        return self.nmd_msg_counter_by_user_in_room[msg_info.room_id][msg_info.user_id] >= USER_NMD_MSGS_CRITERIA
