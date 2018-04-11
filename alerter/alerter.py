import datetime as dt

from alerter import nmd_alerter, tec_alerter, idleness_alerter
from alerter import alerter_util as au
from message_info import MessageType
from critical_moment import CriticalMoment

TIME_BETWEEN_ALERTS_IN_SECONDS = 180


class Alerter:
    def __init__(self):
        self.nmd_alerter = nmd_alerter.NMDAlerter()
        self.tec_alerter = tec_alerter.TECAlerter()
        self.idleness_alerter = idleness_alerter.IdlenessAlerter()
        self.last_alert_in_rooms = {}

    def handle_message_tag(self, msg_info):
        if msg_info.msg_type is MessageType.CHECK_DS:
            self.last_alert_in_rooms[msg_info.room_id] = msg_info.timestamp
            return CriticalMoment.DS

        if msg_info.msg_type is MessageType.TEXT:
            nmd_critical_moment = self.nmd_alerter.handle_message_tag(msg_info)
            tec_critical_moment = self.tec_alerter.handle_message_tag(msg_info)

            if tec_critical_moment is CriticalMoment.TEC and self.should_alert(msg_info):
                self.last_alert_in_rooms[msg_info.room_id] = msg_info.timestamp
                return CriticalMoment.TEC
            if nmd_critical_moment is CriticalMoment.NMD and self.should_alert(msg_info):
                self.last_alert_in_rooms[msg_info.room_id] = msg_info.timestamp
                return CriticalMoment.NMD

        self.idleness_alerter.handle_message_tag(msg_info)

        return CriticalMoment.NONE

    def check_idleness(self):
        current_datetime = dt.datetime.now()
        idle_room_ids = self.idleness_alerter.check_idleness(current_datetime)
        res_idle_room_ids = []

        for room_id in idle_room_ids:
            if self.is_first_alert(room_id) or self.is_enough_time_passed_since_last_alert(room_id, current_datetime):
                self.last_alert_in_rooms[room_id] = current_datetime
                res_idle_room_ids.append(room_id)

        return res_idle_room_ids

    def check_idleness_for_test(self, room_id, timestamp):
        return self.idleness_alerter.check_idleness_in_specific_room(room_id, timestamp)

    def is_first_alert(self, room_id):
        return room_id not in self.last_alert_in_rooms.keys()

    def is_enough_time_passed_since_last_alert(self, room_id, timestamp):
        return au.out_time_interval(self.last_alert_in_rooms[room_id], timestamp, TIME_BETWEEN_ALERTS_IN_SECONDS)

    def should_alert(self, msg_info):
        return self.is_first_alert(msg_info.room_id)\
               or (not self.is_first_alert(msg_info.room_id)
                   and self.is_enough_time_passed_since_last_alert(msg_info.room_id, msg_info.timestamp))
